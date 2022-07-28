from django.contrib import admin
from .models import *
# Register your models here.

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id','instock','outgoing','avialable_stock','avialable_stock_cost')
    search_fields = ['product_id']
    ordering = ['-id']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date','customer','gross_price','total_price','amount_paid','balance')
    search_fields = ['id','customer__name']
    ordering = ['-id']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','unit_price')
    search_fields = ['id','name']
    ordering = ['-id']

admin.site.register(Inventory,InventoryAdmin)
admin.site.register(Inventory_records)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Order_Details)
admin.site.register(Closing_stocks)
admin.site.register(BClosing_Stock_summery)
admin.site.register(BOpening_Stock_summery)
admin.site.register(UserShift)