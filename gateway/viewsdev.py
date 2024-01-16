from django.shortcuts import render
from gateway.models import Merchant
from gateway.tphelperdev import getVars, getHashDigest, postCheckHash, serverCheckHash, curlCallback, serverCheckHash, sendToMerch
from django.views.decorators.csrf import csrf_exempt
import urllib.parse


@csrf_exempt
def index(request):

    index_context = getVars()
    index_context.update({'merch_hashdigest' : getHashDigest(index_context)})

    return render(request, 'index.html', context=index_context)


@csrf_exempt
def callback(request):

    vars = getVars()
    callback_context = {
    'text_OrderID' : 'Order ID: ',
    'text_AddressNumericCheckResult' : 'Address Numeric Check: ',
    'text_PostCodeCheckResult' : 'Post Code Check: ',
    'text_CV2CheckResult' : 'CV2 Check: ',
    'text_ThreeDSecureAuthenticationCheckResult' : 'ThreeD Secure Authentication Check: ',
    'text_Message' : 'Transaction successful!'
    }

    queryset = Merchant.objects.all()
    merch_info = queryset.get()

    if merch_info.ResultDeliveryMethod == "POST":

        requestDict = request.POST.dict()

        print("POST MODE")
        print('############################## Request variables (POST) ###############################')
        print(requestDict)
        print('#######################################################################################')


        if postCheckHash(vars, requestDict) == True:

            callback_context.update(requestDict)

        else:

            callback_context = {
            'text_OrderID' : '',
            'text_AddressNumericCheckResult' : '',
            'text_PostCodeCheckResult' : '',
            'text_CV2CheckResult' : '',
            'text_ThreeDSecureAuthenticationCheckResult' : '',
            'text_Message' : 'Hash check failed.'
            }

        callback_status = request.POST.get('StatusCode')
        callback_message = request.POST.get('Message')
        callback_addcheck = request.POST.get('AddressNumericCheckResult')
        callback_postcheck = request.POST.get('PostCodeCheckResult')
        callback_3dsecure = request.POST.get('ThreeDSecureAuthenticationCheckResult')
        callback_cv2check = request.POST.get('CV2CheckResult')

        sendToMerch(requestDict, callback_status, callback_message, callback_addcheck, callback_postcheck, callback_3dsecure, callback_cv2check)


    elif merch_info.ResultDeliveryMethod == "SERVER_PULL":

        requestDict = request.GET.dict()

        print("SERVER_PULL MODE")
        print('########################### Request variables (SERVER_PULL) ###########################')
        print(requestDict)
        print('#######################################################################################')

        if serverCheckHash(vars,
                    request.GET.get('MerchantID'),
                    request.GET.get('CrossReference'),
                    request.GET.get('OrderID'),
                    request.GET.get('HashDigest')) == True:

            PostString = ("&MerchantID=" + urllib.parse.quote(vars['merch_mid']) +
                          "&Password=" + urllib.parse.quote(vars['merch_password']) +
                          "&CrossReference=" +  urllib.parse.quote(request.GET.get('CrossReference')))

            if 'AddressNumericCheckResult' not in curlCallback(PostString):
                callback_context = {
                'text_OrderID' : 'Order ID: ',
                'text_Message' : 'Transaction successful!  However some variables have not been returned by cURL.  This may be an issue with your hosting provider.'
                }

            callback_context.update(curlCallback(PostString))

        else:
            callback_context = {
            'text_OrderID' : '',
            'text_AddressNumericCheckResult' : '',
            'text_PostCodeCheckResult' : '',
            'text_CV2CheckResult' : '',
            'text_ThreeDSecureAuthenticationCheckResult' : '',
            'text_Message' : 'Hash check failed.'
            }

        callback_status = request.GET.get('StatusCode')
        callback_message = request.GET.get('Message')
        callback_addcheck = request.GET.get('AddressNumericCheckResult')
        callback_postcheck = request.GET.get('PostCodeCheckResult')
        callback_3dsecure = request.GET.get('ThreeDSecureAuthenticationCheckResult')
        callback_cv2check = request.GET.get('CV2CheckResult')

        sendToMerch(requestDict, callback_status, callback_message, callback_addcheck, callback_postcheck, callback_3dsecure, callback_cv2check)

    elif vars['merch_resultdeliverymethod'] == 'SERVER':

        requestDict = request.GET.dict()

        # Check SERVER hash
        if serverCheckHash(vars,
                    request.GET.get('MerchantID'),
                    request.GET.get('CrossReference'),
                    request.GET.get('OrderID'),
                    request.GET.get('HashDigest')) == True:

            callback_context = {
            'text_OrderID' : 'Order ID: ',
            'Message' : 'Transaction successful!  The transaction response from the dummy server used in the demo is empty by default.'
            }

            callback_context.update(requestDict)

        else:
            callback_context = {
            'text_OrderID' : '',
            'text_AddressNumericCheckResult' : '',
            'text_PostCodeCheckResult' : '',
            'text_CV2CheckResult' : '',
            'text_ThreeDSecureAuthenticationCheckResult' : '',
            'text_Message' : 'Hash check failed.'
            }

    if 'AuthCode' not in callback_context['Message']:
             callback_context['text_Message'] = ''

    return render(request, "callback.html", context=callback_context)


@csrf_exempt
def callbackServer(request):

    vars = getVars()
    requestDict = request.POST.dict()

    print("SERVER MODE")
    print('############################# Request variables (SERVER) ##############################')
    print(requestDict)
    print('#######################################################################################')

    if postCheckHash(vars, requestDict) == True:


        callback_status = request.POST.get('StatusCode')
        callback_message = request.POST.get('Message')
        callback_addcheck = request.POST.get('AddressNumericCheckResult')
        callback_postcheck = request.POST.get('PostCodeCheckResult')
        callback_3dsecure = request.POST.get('ThreeDSecureAuthenticationCheckResult')
        callback_cv2check = request.POST.get('CV2CheckResult')

        # Send form data to merchant server
        sendToMerch(requestDict, callback_status, callback_message, callback_addcheck, callback_postcheck, callback_3dsecure, callback_cv2check)

    return render(request, "callback-server.html")
