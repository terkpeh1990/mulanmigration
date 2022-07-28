from django.contrib import admin
from .models import *
# Register your models here.

class RevenueAdmin(admin.ModelAdmin):
    list_display = ('id','created_date' ,'account_code','amount','company','status')
    list_filter = ('company','status','created_date')
    search_fields = ['id','amount','company','status']
    ordering = ['-id']


class GeneralLedgerAdmin(admin.ModelAdmin):
    list_display = ('id','transaction_date' ,'sub_code','description','debit','cedit')
    list_filter = ('transaction_date','sub_code',)
    search_fields = ['id','sub_code','transaction_date']
    ordering = ['-id']

class Bank_CashAdmin(admin.ModelAdmin):
    list_display = ('id','transaction_date' ,'sub_code','description','amount')
    list_filter = ('transaction_date','sub_code',)
    search_fields = ['id','sub_code','transaction_date']
    ordering = ['-id']

class FeesAdmin(admin.ModelAdmin):
    list_display = ('id','transaction_date' ,'amount','balance','student_id')
    list_filter = ('transaction_date',)
    search_fields = ['id','student_id','transaction_date']
    ordering = ['-id']


admin.site.register(Accounts)
admin.site.register(General_Ledger,GeneralLedgerAdmin)
admin.site.register(Bank_Cash_Ledger,Bank_CashAdmin)
admin.site.register(ARevenue,RevenueAdmin)
admin.site.register(fees_transaction,FeesAdmin)
admin.site.register(Payment_Vouchers)
admin.site.register(Transfers)


