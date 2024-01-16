from django.contrib import admin
# from gateway.models import Merchant
# from models import Merchant
from .models import Merchant

#admin.site.register(Merchant)
# admin.site.register(Password)
# admin.site.register(Preshared)

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('MID', 'Password', 'Preshared', 'HashMethod', 'ResultDeliveryMethod', 'TransactionType')
    #inlines = [BookInstanceInline]
