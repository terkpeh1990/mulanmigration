from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SalonProduct)
admin.site.register(SalonInventory)
admin.site.register(SalonClosing_stocks)
admin.site.register(SalonInventory_records)
admin.site.register(SalonOrder)
admin.site.register(SalonOrder_Details)

