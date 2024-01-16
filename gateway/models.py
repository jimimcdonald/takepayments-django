from django.db import models

class Merchant(models.Model):

    """Model representing a specific merchant"""
    MID = models.CharField(max_length = 14, help_text="Enter your Merchant ID code")
    Password = models.CharField(max_length = 50, help_text="Enter your password", default='password')
    Preshared = models.CharField(max_length = 50, help_text="Enter your preshared key", default='preshared key')
    TransactionType = models.CharField(max_length = 50, help_text="Enter transaction type", default='SALE')
    HashMethod = models.CharField(max_length = 50, choices=[('MD5', 'MD5'), ('SHA1', 'SHA1'),('HMACMD5', 'HMACMD5'),
        ('HMACSHA1', 'HMACSHA1'), ('HMACSHA256', 'HMACSHA256'), ('HMACSHA512', 'HMACSHA512')])
    ResultDeliveryMethod = models.CharField(max_length = 50, choices=[('POST', 'POST'), ('SERVER_PULL', 'SERVER_PULL'), ('SERVER', 'SERVER')])


    def __str__(self):
        return self.MID
