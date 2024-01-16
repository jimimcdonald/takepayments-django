import hmac
import datetime
import tzlocal
import hashlib
import pycurl
import simplejson as json
from io import BytesIO
from .models import Merchant

def getVars():

    # Set time
    present_time = datetime.datetime.now(tzlocal.get_localzone())

    ## Get data from Merchant class
    ## Uncomment when using Flask, replace in vars dict below
    # from gateway.models import Merchant

    queryset = Merchant.objects.all()
    merch_info = queryset.get()
    merch_mid = merch_info.MID
    merch_password = merch_info.Password
    merch_presharedkey = merch_info.Preshared
    merch_hashmethod = merch_info.HashMethod
    merch_resultdeliverymethod = merch_info.ResultDeliveryMethod
    merch_transactiontype = merch_info.TransactionType

    # Create form variables
    vars = {
        'merch_mid' : merch_mid,
        'merch_password' : merch_password,
        'merch_presharedkey' : merch_presharedkey,
        'merch_amt' : '1234',
        'merch_orderid' : 'Order-123',
        'merch_transactiontype' : merch_transactiontype,
        'merch_currencycode' : '826',
        'merch_transactiondatetime' : present_time.strftime("%Y-%m-%d %H:%M:%S %z"),
        'merch_orderdesc' : 'Order description',
        'merch_customername' : 'Geoff Wayne',
        'merch_address1' : '113 Broad Street West',
        'merch_address2' : 'Old pine',
        'merch_address3' : 'Strongbarrow',
        'merch_address4' : 'AddFour',
        'merch_city' : 'City',
        'merch_state' : 'State',
        'merch_postcode' : 'SB42 1SX',
        'merch_countrycode' : '826',
        'merch_hashmethod' : merch_hashmethod,
        'merch_callbackurl' : 'http://127.0.0.1:8000/gateway/callback/', #
        #'merch_callbackurl' : 'http://takepayments-python-django.herokuapp.com/gateway/callback/',
        'merch_echoavs' : 'true',
        'merch_echocv2' : 'true',
        'merch_echothreed' : 'true',
        'merch_echocardtype' : 'true',
        'merch_echocardtype' : 'true',
        'merch_cv2mandatory' : 'true',
        'merch_address1mandatory' : 'true',
        'merch_citymandatory' : 'true',
        'merch_postcodemandatory' : 'true',
        'merch_statemandatory' : 'true',
        'merch_countrymandatory' : 'true',
        'merch_resultdeliverymethod' : merch_resultdeliverymethod,
        'merch_serverresulturl' : 'http://127.0.0.1/callback-server/', #'http://takepayments-python-django.herokuapp.com/gateway/callback-server/',
        'merch_paymentformsdisplaysresult' : 'false',
        'merch_serverresulturlcookievariables' : '',
        'merch_serverresulturlformvariables' : '',
        'merch_serverresulturlquerystringvariables' : '',
    }
    return vars


def calculateHashDigest(stringtohash, key, hashmethod):

    strkey = "PreSharedKey=" + key + "&"

    if hashmethod == "MD5":
    	hash = hashlib.md5((strkey+stringtohash).encode('utf-8'))

    elif hashmethod == "SHA1":
    	hash = hashlib.sha1((strkey+stringtohash).encode('utf-8'))

    elif hashmethod == "HMACMD5":
        hash = hmac.new(bytes(key.encode('utf-8')), bytes(stringtohash.encode('utf-8')), hashlib.md5)

    elif hashmethod == "HMACSHA1":
        hash = hmac.new(bytes(key.encode('utf-8')), bytes(stringtohash.encode('utf-8')), hashlib.sha1)

    elif hashmethod == "HMACSHA256":
        hash = hmac.new(bytes(key.encode('utf-8')), bytes(stringtohash.encode('utf-8')), hashlib.sha256)

    elif hashmethod == "HMACSHA512":
        hash = hmac.new(bytes(key.encode('utf-8')), bytes(stringtohash.encode('utf-8')), hashlib.sha512)

    return hash.hexdigest()


def getHashDigest(vars):

    # Generates the initial hashdigest for payment form
    StringToHash = ("MerchantID=" + vars['merch_mid'] +
        "&Password=" + vars['merch_password'] + "&Amount=" + vars['merch_amt'] + "&CurrencyCode=" + vars['merch_currencycode'] +
        "&EchoAVSCheckResult=" + vars['merch_echoavs'] + "&EchoCV2CheckResult=" + vars['merch_echocv2'] +
        "&EchoThreeDSecureAuthenticationCheckResult=" + vars['merch_echothreed'] + "&EchoCardType=" + vars['merch_echocardtype'] +
        "&OrderID=" + vars['merch_orderid'] + "&TransactionType=" + vars['merch_transactiontype'] + "&TransactionDateTime=" + vars['merch_transactiondatetime'] +
        "&CallbackURL=" + vars['merch_callbackurl'] + "&OrderDescription=" + vars['merch_orderdesc'] + "&CustomerName=" + vars['merch_customername'] +
        "&Address1=" + vars['merch_address1'] + "&Address2=" + vars['merch_address2'] + "&Address3=" + vars['merch_address3'] + "&Address4=" + vars['merch_address4'] +
        "&City=" + vars['merch_city'] + "&State=" + vars['merch_state'] + "&PostCode=" + vars['merch_postcode'] + "&CountryCode=" + vars['merch_countrycode'] +
        "&CV2Mandatory=" + vars['merch_cv2mandatory'] + "&Address1Mandatory=" + vars['merch_address1mandatory'] + "&CityMandatory=" + vars['merch_citymandatory'] +
        "&PostCodeMandatory=" + vars['merch_postcodemandatory'] + "&StateMandatory=" + vars['merch_statemandatory'] +
        "&CountryMandatory=" + vars['merch_countrymandatory'] + "&ResultDeliveryMethod=" + vars['merch_resultdeliverymethod'] +
        "&ServerResultURL=" + vars['merch_serverresulturl'] + "&PaymentFormDisplaysResult=" + vars['merch_paymentformsdisplaysresult'] +
        "&ServerResultURLCookieVariables=" + vars['merch_serverresulturlcookievariables'] +
        "&ServerResultURLFormVariables=" + vars['merch_serverresulturlformvariables'] +
        "&ServerResultURLQueryStringVariables=" + vars['merch_serverresulturlquerystringvariables'])

    # Send string to hash method
    HashDigest = calculateHashDigest(StringToHash, vars['merch_presharedkey'], vars['merch_hashmethod'])

    return HashDigest


def curlCallback(PostString):

    # Set up curl
    b = BytesIO()
    c = pycurl.Curl()

    c.setopt(pycurl.URL, "https://mms.tponlinepayments2.com/Pages/PublicPages/PaymentFormResultHandler.ashx")
    c.setopt(pycurl.POST, True)
    c.setopt(pycurl.POSTFIELDS ,PostString)
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    curl_error = pycurl.error
    curl_info = c.getinfo(c.RESPONSE_CODE)
    response = b.getvalue().decode('UTF-8')
    c.close()

    #Parse succesful curl response
    parsed = parseResponse(response)

    # Create callback context from results of parsed curl response
    if 'AddressNumericCheckResult' in parsed:
        callback_context = {
            'Message' : parsed['Message'],
            'PreviousStatusCode' : parsed['PreviousStatusCode'],
            'PreviousMessage' : parsed['PreviousMessage'],
            'CrossReference' : parsed['CrossReference'],
            #-------------------these variables not always returned ----------------
            'AddressNumericCheckResult' : parsed['AddressNumericCheckResult'],
            'PostCodeCheckResult' : parsed['PostCodeCheckResult'],
            'CV2CheckResult' : parsed['CV2CheckResult'],
            'ThreeDSecureAuthenticationCheckResult' : parsed['ThreeDSecureAuthenticationCheckResult'],
            'CardType' : parsed['CardType'],
            'CardClass' : parsed['CardClass'],
            'CardIssuer' : parsed['CardIssuer'],
            'CardIssuerCountryCode' : parsed['CardIssuerCountryCode'],
            #-----------------------------------------------------------------------
            'Amount' : parsed['Amount'],
            'CurrencyCode' : parsed['CurrencyCode'],
            'OrderID' : parsed['OrderID'],
            'TransactionType' : parsed['TransactionType'],
            'TransactionDateTime' : parsed['TransactionDateTime'],
            'OrderDescription' : parsed['OrderDescription'],
            'CustomerName' : parsed['CustomerName'],
            'Address1' : parsed['Address1'],
            'Address2' : parsed['Address2'],
            'Address3' : parsed['Address3'],
            'Address4' : parsed['Address4'],
            'City' : parsed['City'],
            'State' : parsed['State'],
            'PostCode' : parsed['PostCode'],
            'CountryCode' : parsed['CountryCode']
        }

    else:
        callback_context = {
            'Message' : parsed['Message'],
            'PreviousStatusCode' : parsed['PreviousStatusCode'],
            'PreviousMessage' : parsed['PreviousMessage'],
            'CrossReference' : parsed['CrossReference'],
            #-----------------------------------------------------------------------
            'Amount' : parsed['Amount'],
            'CurrencyCode' : parsed['CurrencyCode'],
            'OrderID' : parsed['OrderID'],
            'TransactionType' : parsed['TransactionType'],
            'TransactionDateTime' : parsed['TransactionDateTime'],
            'OrderDescription' : parsed['OrderDescription'],
            'CustomerName' : parsed['CustomerName'],
            'Address1' : parsed['Address1'],
            'Address2' : parsed['Address2'],
            'Address3' : parsed['Address3'],
            'Address4' : parsed['Address4'],
            'City' : parsed['City'],
            'State' : parsed['State'],
            'PostCode' : parsed['PostCode'],
            'CountryCode' : parsed['CountryCode']
        }

    return callback_context


def parseResponse(string):

    # Takes in the cUrl response string and returns json format dict
    index = string.find('MerchantID')
    string = (string[index:])

    string = string.replace('%3d', '" : "')
    string = string.replace('%26', '", "')
    string = string.replace('%3a', ':')
    string = string.replace('+', ' ')
    string = string.replace('%2b', '+')
    string = '{ "' + string + '" }'

    newdict = json.loads(string)

    return newdict


def postCheckHash(vars, request):

    HashDigest = request['HashDigest']

    StringToHash = ("MerchantID=" + vars['merch_mid'] +
                    "&Password=" + vars['merch_password'] +
                    "&StatusCode=" + request['StatusCode'] +
                    "&Message=" + request['Message'] +
                    "&PreviousStatusCode=" + request['PreviousStatusCode'] +
                    "&PreviousMessage=" + request['PreviousMessage'] +
                    "&CrossReference=" + request['CrossReference'] +
                    "&AddressNumericCheckResult=" + request['AddressNumericCheckResult'] +
                    "&PostCodeCheckResult=" + request['PostCodeCheckResult'] +
                    "&CV2CheckResult=" + request['CV2CheckResult'] +
                    "&ThreeDSecureAuthenticationCheckResult=" + request['ThreeDSecureAuthenticationCheckResult'] +
                    "&CardType=" + request['CardType'] +
                    "&CardClass=" + request['CardClass'] +
                    "&CardIssuer=" + request['CardIssuer'] +
                    "&CardIssuerCountryCode=" + request['CardIssuerCountryCode'] +
                    "&Amount=" + request['Amount'] +
                    "&CurrencyCode=" + request['CurrencyCode'] +
                    "&OrderID=" + request['OrderID'] +
                    "&TransactionType=" + request['TransactionType'] +
                    "&TransactionDateTime=" + request['TransactionDateTime'] +
                    "&OrderDescription=" + request['OrderDescription'] +
                    "&CustomerName=" + request['CustomerName'] +
                    "&Address1=" + request['Address1'] +
                    "&Address2=" + request['Address2'] +
                    "&Address3=" + request['Address3'] +
                    "&Address4=" + request['Address4'] +
                    "&City=" + request['City'] +
                    "&State=" + request['State'] +
                    "&PostCode=" + request['PostCode'] +
                    "&CountryCode=" + request['CountryCode'])

    # Send string to hash method
    NewHashDigest = calculateHashDigest(StringToHash, vars['merch_presharedkey'], vars['merch_hashmethod'])

    if HashDigest == NewHashDigest:
        return True

    else:
        return False


def serverCheckHash(vars, MerchantID, CrossReference, OrderID, HashDigest):

    StringToHash = ("MerchantID=" + MerchantID +
                  "&Password=" + vars['merch_password'] +
                  "&CrossReference=" + CrossReference +
                  "&OrderID=" + OrderID)

    # Send string to hash method
    NewHashDigest = calculateHashDigest(StringToHash, vars['merch_presharedkey'], vars['merch_hashmethod'])

    if HashDigest == NewHashDigest:
        return True

    else:
        return False


def sendToMerch(TransactionCallback, callback_status, callback_message, callback_addcheck, callback_postcheck, callback_3dsecure, callback_cv2check):

    #Currently prints to log in place of server

    # Formats response for user
    if callback_status == '0':
        TransactionOutcome = 'Successful'

    elif callback_status == '3':
        TransactionOutcome = '3D Secure Required'

    elif callback_status == '4':
        TransactionOutcome = 'Referred'

    elif callback_status == '5':
        TransactionOutcome = 'Declined'

    elif callback_status == '20':
        TransactionOutcome = 'Duplicate'

    elif callback_status == '30':
        TransactionOutcome = 'Gateway error'

    elif callback_status == None:
        TransactionOutcome = ''

    elif callback_status == '':
        TransactionOutcome = ''

    else:
        TransactionOutcome = 'Unknown error'

    if callback_addcheck == None: callback_addcheck = 'Check result not returned'
    if callback_3dsecure == None: callback_3dsecure = 'Check result not returned'
    if callback_postcheck == None: callback_postcheck = 'Check result not returned'
    if callback_cv2check == None: callback_cv2check = 'Check result not returned'
    if callback_message == None: callback_message = 'No callback message returned'

    callback_addcheck = "Address numeric check - " + callback_addcheck + " | "
    callback_3dsecure = "3D secure authentication - " + callback_3dsecure + " | "
    callback_postcheck = "Postcode check - " + callback_postcheck + " | "
    callback_cv2check = "CV2 check - " + callback_cv2check

    TransactionOutcomeDetail = "| " + callback_message + " | " + callback_addcheck + callback_3dsecure + callback_postcheck + callback_cv2check

    print("######################### sendToMerch() has just sent... ##############################")
    print(TransactionCallback)
    print(TransactionOutcome)
    print(TransactionOutcomeDetail)
    print("########################### ...to Merchant's Server ###################################")
