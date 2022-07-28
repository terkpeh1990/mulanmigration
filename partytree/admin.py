from django.contrib import admin
from .models import *
# Register your models here.

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id','instock','outgoing','avialable_stock','avialable_stock_cost')
    search_fields = ['product_id__name']
    ordering = ['-id']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','unit_price')
    search_fields = ['id','name']
    ordering = ['-id']


admin.site.register(Inventorys,InventoryAdmin)
admin.site.register(Inventory_recordss)
admin.site.register(Categorys)
admin.site.register(Products,ProductAdmin)
admin.site.register(Orders)
admin.site.register(Order_Detailss)
admin.site.register(Damagess)
admin.site.register(Closing_stockss)
admin.site.register(Closing_Stock_summery)
admin.site.register(Opening_Stock_summery)