from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .import supervisor
from .import cashier


app_name = 'salon'

urlpatterns = [
    path('manage_category/', supervisor.manage_category, name='manage_category'),
    path('create_category/', supervisor.create_category, name='create_category'),
    path('edit_category/<str:pk>/', supervisor.edit_category, name='edit_category'),
    path('manage_product/', supervisor.manage_product, name='manage_product'),
    path('create_product/', supervisor.create_product, name='create_product'),
    path('edit_product/<str:pk>/', supervisor.edit_product, name='edit_product'),

    path('create_customer/', cashier.create_customer, name='create_customer'),
    path('orderitems/', cashier.orderitems.as_view(), name='orderitems'),
    path('delete_item/<str:pk>/', cashier.deletes, name='delete_item'),
    path('checkout/', cashier.checkout, name='checkout'),
    path('checkout_print/<str:pk>/', cashier.checkout_print, name='checkout_print'),
    path('Vew_order/<str:pk>/', cashier.Vew_order, name='Vew_order'),
    path('close_order', cashier.close_order, name='close_order'),
    path('close', cashier.close, name='close'),
    path('manage_order', cashier.manage_order, name='manage_order'),
    path('makepayment/<str:pk>/', cashier.makepayment, name='makepayment'),

    path('create_restock/', supervisor.create_restock, name='create_restock'),
    path('approve_restock/<str:pk>/',
         supervisor.approve_restock, name='approve_restock'),
    path('cancel_restock/<str:pk>/',
         supervisor.cancel_restock, name='cancel_restock'),
    path('manage_restock/', supervisor.manage_restock, name='manage_restock'),

    path('manage_inventory/', supervisor.manage_inventory, name='manage_inventory'),
    path('EditInventory/<str:pk>/', supervisor.EditInventory, name='EditInventory'),
    path('closing_stock/', supervisor.closing_stock, name='closing_stock'),
    path('closed_stock/', supervisor.closed_stock, name='closed_stock'),

    path('pending_restock/', supervisor.pending_restock, name='pending_restock'),
    path('daily_sales/', supervisor.daily_sales, name='daily_sales'),
    path('taxation/', supervisor.taxation, name='taxation'),


]
