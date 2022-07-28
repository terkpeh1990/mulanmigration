from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from .forms import *
from .models import *
from salon import *
from school.models import *
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, View, CreateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.core import serializers
import datetime
from django.contrib.auth.decorators import login_required
from school_management_system.settings import TWILIO_ACCOUNT_SID4, TWILIO_AUTH_TOKEN4, TWILIO_PHONE_NUMBER4
from twilio.rest import Client
# from .filters import *


# @login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now().date()
            customer = form.save()
            order = SalonOrder.objects.create(
                customer=customer, order_date=today, due_date=customer.due_dates)
            print(customer)
            request.session['id'] = order.id
            return redirect('salon:orderitems')

    else:
        form = CustomerForm()

    template = 'salon/customer.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# def orderitems(request):
#     if request.session['id']:
#         order_id = request.session['id']
#         order = Order.objects.get(id=order_id)
#         detail = Order_Details.objects.filter(order_id=order)
#         list_inventory = Inventory.objects.filter(avialable_stock__gt=0)
#         gross_total = detail.aggregate(cc=Sum('gross_price'))
#         if not gross_total['cc']:
#             vat = 0.00
#         else:
#             vat = float(gross_total['cc']) * 0.03
#         if not gross_total['cc']:
#             total_sum = 0.00 + vat
#         else:
#             total_sum = float(gross_total['cc']) + vat
#         if not gross_total['cc']:
#             order.gross_price = 0
#         else:
#             order.gross_price = gross_total['cc']
#         order.vat = vat
#         order.save()
#     template = 'backery/create_order.html'
#     context = {
#         "detail": detail,
#         "vat": vat,
#         "total_sum": total_sum,
#         "order": order,
#         "list_inventory": list_inventory,
#     }
#     return render(request, template, context)


# def add_items_to_chart(request, pk):
#     if request.session['id']:
#         order_id = request.session['id']
#         order = Order.objects.get(id=order_id)
#         get_inventory = Inventory.objects.get(id=pk)
#         get_product = Product.objects.get(name=get_inventory.product_id.name)
#         details = Order_Details.objects.create(
#             product=get_product, unit_price=get_product.unit_price, quantity=1, gross_price=get_product.unit_price, order_id=order)
#         # get_inventory.instock -= 1
#         get_inventory.outgoing += 1
#         get_inventory.save()
#         print(get_inventory.instock)
#         get_product.save()
#         Inventory_records.objects.create(
#             product=get_product, quantity=details.quantity, unit_price=get_product.unit_price, status="Outgoing")
#         messages.success(request, "Item Added To Chart")
#         return redirect('shop:orderitems')

class orderitems(CreateView):
    model = Order_Details
    form_class = OrderdetailsForm
    template = 'salon/create_order.html'

    def get(self, *args, **kwargs):
        if self.request.session['id']:
            order_id = self.request.session['id']
            order = SalonOrder.objects.get(id=order_id)
            form = self.form_class()
            detail = SalonOrder_Details.objects.filter(order_id=order)
            gross_total = detail.aggregate(cc=Sum('gross_price'))
            vat =  0.00
            if not gross_total['cc']:
                total_sum = 0.00
            else:
                total_sum = float(gross_total['cc'])
            if not gross_total['cc']:
                order.gross_price = 0.00
            else:
                order.gross_price = gross_total['cc']
            order.vat = vat
            order.save()
            return render(self.request, self.template, {"form": form, "detail": detail, "vat": vat, "total_sum": total_sum, "order": order})

    def post(self,  *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if self.request.session['id']:
                order_id = self.request.session['id']
                order = SalonOrder.objects.get(id=order_id)
            if form.is_valid():

                instance = form.save(commit=False)
                product = SalonProduct.objects.get(name=instance.product)
                product_unit_price = product.unit_price
                instance.order_id = order
                instance.unit_price = product_unit_price
                instance.gross_price = product_unit_price * instance.quantity
                instance.save()
                if product.category.name == 'Products':
                    get_product = SalonInventory.objects.get(product_id=product.id)
                    get_product.outgoing += instance.quantity
                    get_product.save()
                    SalonInventory_records.objects.create(
                        product=product, quantity=instance.quantity, unit_price=product.unit_price, status="Outgoing", approval="Approved")
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self, form):
        messages.success(self.request, 'Sales item added')
        return super().form_valid(form)


# @login_required
def deletes(request, pk):
    pro = SalonOrder_Details.objects.get(id=pk)
    product = SalonProduct.objects.get(name=pro.product)
    if product.category.name == 'Products':
        get_product = SalonInventory.objects.get(product_id=product.id)
        get_product.instock += pro.quantity
        get_product.save()
        SalonInventory_records.objects.create(
            product=product, quantity=pro.quantity, unit_price=product.unit_price, status="Incoming")
    pro.delete()
    return redirect('salon:orderitems')


# @login_required
def checkout(request):
    if request.session['id']:
        order_id = request.session['id']
        order = SalonOrder.objects.get(id=order_id)
        detail = SalonOrder_Details.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            order.amount_paid = form.cleaned_data['amount_paid']
            order.save()

            try:
                code = Account_code.objects.get(code="Sales")
            except Account_code.DoesNotExist:
                code = Account_code.objects.create(code="Sales")
            company = Company_group.objects.get(name="Irish Green")
            Revenue.objects.create(
                account_code=code, amount=order.amount_paid, company=company)
            client = Client(TWILIO_ACCOUNT_SID4, TWILIO_AUTH_TOKEN4)
            #  ,http_client=proxy_client
            today = datetime.datetime.now().date()

            try:
                message = client.messages.create(
                    to="+233" + order.customer.phone,
                    from_=TWILIO_PHONE_NUMBER4,
                    body="Dear" + " " + order.customer.name + "," + " " + "The total cost of service rended to you with ID" + " "+order.id + " " + "is " + " " + "GHC" + " " + str(order.total_price) + " " + " You have made payment of GHC" + " " + str(order.amount_paid) + " " + ".Thank you for choosing Irish Green Spa, For enquiries and orders, Please contact us on 0302943465.")
            except IOError:
                print('fail')
                pass


    else:
        form = PaymentForm()
    template = 'salon/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)


# @login_required
def checkout_print(request, pk):

    order = SalonOrder.objects.get(id=pk)
    detail = SalonOrder_Details.objects.filter(order_id=order.id)
    template = 'salon/checkout_print.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


# @login_required
def Vew_order(request, pk):

    order = SalonOrder.objects.get(id=pk)
    detail = SalonOrder_Details.objects.filter(order_id=order.id)
    template = 'salon/view_order.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


# @login_required
def close_order(request):
    if request.session['id']:
        try:
            del request.session['id']
            return redirect('salon:manage_order')
        except KeyError:
            return redirect('salon:manage_order')


# @login_required
def close(request):
    return redirect('salon:manage_order')


# @login_required
def manage_order(request):

    orders = SalonOrder.objects.all().order_by('-id')
    template = 'salon/manage_orders.html'
    context = {
        'orders': orders,
    }
    return render(request, template, context)



# @login_required
def makepayment(request, pk):
    order = SalonOrder.objects.get(id=pk)
    detail = SalonOrder_Details.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            dd = form.cleaned_data['amount_paid']
            order.amount_paid += form.cleaned_data['amount_paid']
            order.save()
            try:
                code = Account_code.objects.get(code="Sales")
            except Account_code.DoesNotExist:
                code = Account_code.objects.create(code="Sales")
            company = Company_group.objects.get(name="Irish Green")
            Revenue.objects.create(
                account_code=code, amount=dd, company=company)
            client = Client(TWILIO_ACCOUNT_SID4, TWILIO_AUTH_TOKEN4)
            try:
                message = client.messages.create(
                    to="+233" + order.customer.phone,
                    from_=TWILIO_PHONE_NUMBER4,
                    body="Dear" + " " + order.customer.name + "," + " " + "The total cost of service rendered to you with ID" + " "+order.id + " " + "is " + " " + "GHC" + " " + str(order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(order.amount_paid) + " " + ".Thank you for choosing Irish Green Spa, For enquiries and orders, Please contact us on 0302943465.")
            except IOError:
                print('fail')
                pass

            messages.success(request, 'Payment made Sucessfully')
            return redirect('salon:manage_order')
    else:
        form = PaymentForm()
    template = 'salon/check.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)


