from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from .forms import *
from .models import *
from bakery import *
from school.models import *
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, View, CreateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.core import serializers
import datetime
from django.contrib.auth.decorators import login_required
from school_management_system.settings import TWILIO_ACCOUNT_SID2, TWILIO_AUTH_TOKEN2, TWILIO_PHONE_NUMBER2
from twilio.rest import Client
from .filters import *
from .thread import *
from accounts.models import Account_Receivable, General_Ledger, Sub_Accounts,Bank_Cash_Ledger,ARevenue #new

@login_required
def create_customer(request):
    if request.method == 'POST':

        form = CustomerForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now().date()
            customer = form.save()
            vv = UserShift.objects.all().order_by('id')
            bb=vv.last()
            order = Order.objects.create(customer=customer, order_date=today, due_date=customer.due_dates,usershift=bb,ordertype='Internal',gross_price=0.00)
            print(customer)

            if customer.due_dates:
                return redirect('shop:tadd_items_to_charts',order.id)
            else:
                return redirect('shop:add_items_to_charts',order.id)

    elif UserShift.objects.all().order_by('id').last().status == 'Closed':
        vv = UserShift.objects.all().order_by('id')
        bb=vv.last()
        print(bb.id)
        messages.success(request,'You cannot Create any Order till you start your shift')
        return redirect('shop:manage_order')

    elif UserShift.objects.all().order_by('id').last().profile != request.user.profile:
        messages.success(request,'You cannot Sell while another person shift is still active')
        return redirect('shop:manage_order')


    else:
        form = CustomerForm()

    template = 'backery/customer.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def jumai_order(request):
    if UserShift.objects.all().order_by('id').last().status == 'Closed':
        vv = UserShift.objects.all().order_by('id')
        bb=vv.last()
        print(bb.id)
        messages.success(request,'You cannot Create any Order till you start your shift')
        return redirect('shop:manage_order')

    elif UserShift.objects.all().order_by('id').last().profile != request.user.profile:
        messages.success(request,'You cannot Sell while another person shift is still active')
        return redirect('shop:manage_order')

    else:
        today = datetime.datetime.now().date()
        vv = UserShift.objects.all().order_by('id')
        bb=vv.last()
        order = Order.objects.create( order_date=today,usershift=bb,ordertype='Jumia',gross_price=0.00)
        return redirect('shop:add_items_to_charts',order.id)


def cancel_order(request,pk):
    order = Order.objects.get(id=pk)
    details = Order_Details.objects.filter(order_id=order.id)
    for a in details:
        get_inventory = Inventory.objects.get(product_id=a.product)
        get_inventory.outgoing -= a.quantity
        get_inventory.save()
        a.delete()
    order.delete()
    messages.success(request,"Order Cancelled")
    return redirect('shop:manage_order')



def add_items_to_charts(request,pk):


    order = Order.objects.get(id=pk)
    try:
        details= Order_Details.objects.filter(order_id=order.id)
        gross_total = details.aggregate(cc=Sum('gross_price'))
        order.gross_price= gross_total['cc']
        order.save()
    except Order_Details.DoesNotExist:
        pass

    if request.method =='POST':
        form=OrderdetailsForm(request.POST)



        if form.is_valid():
            qty = form.cleaned_data.get('quantity')
            a=form.cleaned_data['product']
            print(a)
            item = Product.objects.get(id=a.id)
            if Order_Details.objects.filter(product=item,order_id=order).exists():
                messages.success(request, item.name+" "+"has already been selected")
                return redirect('shop:add_items_to_charts',order.id)
            else:
                get_inventory = Inventory.objects.get(product_id=item.id)

                detailss = Order_Details.objects.create(
                                product=item, unit_price=item.unit_price, quantity=qty, gross_price=(item.unit_price * qty), order_id =order)
                get_inventory.outgoing += qty
                get_inventory.save()
                gross_total = details.aggregate(cc=Sum('gross_price'))
                order.gross_price= gross_total['cc']
                order.save()

                messages.success(request, detailss.product.name +" " +"added successfully")
                return redirect('shop:add_items_to_charts',order.id)
    else:
        form = OrderdetailsForm()

    template = 'backery/create_order.html'
    context ={
            "detail": details,
            "order": order,
            'form':form,


        }
    return render(request, template, context)

class orderitems(CreateView):
    model = Order_Details
    form_class = OrderdetailsForm
    template = 'backery/create_order.html'



    def get(self, *args, **kwargs):
         if self.request.session['id']:
            order_id = self.request.session['id']
            order = Order.objects.get(id=order_id)
            form = self.form_class()
            detail = Order_Details.objects.filter(order_id=order)
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
            return render(self.request, self.template, {"form": form, "detail":detail, "vat": vat,"total_sum":total_sum,"order":order})

    def post(self,  *args, **kwargs):
        if self.request.is_ajax and self.request.method =="POST":
            form = self.form_class(self.request.POST)
            if self.request.session['id']:
                order_id = self.request.session['id']
                order = Order.objects.get(id=order_id)
            if form.is_valid():

                instance = form.save(commit=False)
                product = Product.objects.get(name = instance.product)
                product_unit_price = product.unit_price
                instance.order_id = order
                instance.unit_price = product_unit_price
                instance.gross_price = product_unit_price * instance.quantity
                instance.save()
                get_product = Inventory.objects.get(product_id=product.id)
                get_product.outgoing += instance.quantity
                Inventory_records.objects.create(
                    product=product, quantity=instance.quantity, unit_price=product.unit_price, status="Outgoing")
                get_product.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self,form):
        messages.success(self.request, 'Sales item added')
        return super().form_valid(form)


@login_required
def deletes(request,pk):
    pro = Order_Details.objects.get(id=pk)
    order =Order.objects.get(id=pro.order_id.id)
    product = Product.objects.get(name=pro.product)
    get_product = Inventory.objects.get(product_id=product.id)
    get_product.outgoing -= pro.quantity
    get_product.save()
    Inventory_records.objects.create(
        product=product, quantity=pro.quantity, unit_price=product.unit_price, status="Incoming")
    pro.delete()
    return redirect('shop:add_items_to_charts',order.id)


@login_required
def tdeletes(request,pk):
    pro = Order_Details.objects.get(id=pk)
    order =Order.objects.get(id=pro.order_id.id)
    product = Product.objects.get(name=pro.product)

    # Inventory_records.objects.create(
    #     product=product, quantity=pro.quantity, unit_price=product.unit_price, status="Incoming")
    pro.delete()
    return redirect('shop:tadd_items_to_chart',order.id)


@login_required
# to work on
def checkout(request,pk):

    order = Order.objects.get(id =pk)
    detail = Order_Details.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('shop:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount']
                order.save()

            try:
                code= Sub_Accounts.objects.get(sub_code = 1202)
            except Sub_Accounts.DoesNotExist:
                pass
            try:
                jcode= Sub_Accounts.objects.get(sub_code = 1207)
            except Sub_Accounts.DoesNotExist:
                pass
            company = Company_group.objects.get(name="Party Tree Bakes")
            shifts = UserShift.objects.all().order_by('id')
            shift = shifts.last()
            print(shift.id)

            if order.ordertype == 'Jumia':
                ARevenue.objects.create(
                account_code=jcode, amount=order.amount_paid, company=company,shift=shift,status='Jumia',close='New')
            else:
                ARevenue.objects.create(
                    account_code=code, amount=order.amount_paid, company=company,shift=shift,status='Cash',close='New')
            client = Client(TWILIO_ACCOUNT_SID2, TWILIO_AUTH_TOKEN2)
            # ,http_client=proxy_client
            today = datetime.datetime.now().date()
            CheckoutThread(order).start()

    else:
        form = paymentForm()
    template = 'backery/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request,template,context)


@login_required
# to work on
def momocheckout(request,pk):

    order = Order.objects.get(id =pk)
    detail = Order_Details.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('shop:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount']
                order.save()

            try:
                code= Sub_Accounts.objects.get(sub_code = 1204)
            except Sub_Accounts.DoesNotExist:
                pass
            company = Company_group.objects.get(name="Party Tree Bakes")
            shifts = UserShift.objects.all().order_by('id')
            shift = shifts.last()
            print(shift.id)

            ARevenue.objects.create(
                account_code=code, amount=order.amount_paid, company=company,shift=shift,status='Momo',close='New')
            today = datetime.datetime.now().date()
            CheckoutThread(order).start()

    else:
        form = paymentForm()
    template = 'backery/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request,template,context)

@login_required
def checkout_print(request,pk):

    order = Order.objects.get(id=pk)
    detail = Order_Details.objects.filter(order_id=order.id)
    template = 'backery/checkout_print.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)

@login_required
def Vew_order(request,pk):

    order = Order.objects.get(id=pk)
    detail = Order_Details.objects.filter(order_id=order.id)
    template = 'backery/view_order.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


@login_required
def close_order(request):
    return redirect('shop:manage_order')


@login_required
def close(request):

    return redirect('shop:manage_order')

@login_required
def manage_order(request):
    today =datetime.date.today()
    profile = request.user.profile
    orders = Order.objects.filter(gross_price__gt=0.00,order_date=today,usershift__profile=profile)
    ord = Order.objects.filter(gross_price__gt=0.00,order_date=today,usershift__profile=profile)
    company = Company_group.objects.get(name="Party Tree Bakes")
    to = ord.count()
    grss = ARevenue.objects.filter(company=company.id,status='Cash',
        created_date=today,shift__profile=profile).aggregate(cc=Sum('amount'))
    momo = ARevenue.objects.filter(company=company.id,status='Momo',
        created_date=today,shift__profile=profile).aggregate(bb=Sum('amount'))
    jumia = ARevenue.objects.filter(company=company.id,status='Jumia',
        created_date=today,shift__profile=profile).aggregate(bb=Sum('amount'))
    total = ARevenue.objects.filter(company=company.id,
        created_date=today,shift__profile=profile).aggregate(dd=Sum('amount'))


    orders = Order.objects.filter(clear=False,usershift__profile=profile)
    template = 'backery/manage_orders.html'
    context = {
        'orders': orders,
        'to':to,
        'grss':grss,
        'momo':momo,
        'total':total,
        'jumia':jumia,
    }
    return render(request,template,context)


def tadd_items_to_charts(request,pk):


    order = Order.objects.get(id=pk)
    try:
        details= Order_Details.objects.filter(order_id=order.id)
        gross_total = details.aggregate(cc=Sum('gross_price'))
        order.gross_price= gross_total['cc']
        order.save()
    except Order_Details.DoesNotExist:
        pass


    if request.method =='POST':
        form=TakeOrderdetailsForm(request.POST)



        if form.is_valid():
            qty = form.cleaned_data.get('quantity')
            a=form.cleaned_data['product']
            item = Product.objects.get(id=a.id)
            if Order_Details.objects.filter(product=item,order_id=order).exists():
                messages.success(request, item.name+" "+"has already been selected")
                return redirect('shop:tadd_items_to_charts',order.id)
            else:
                if order.ordertype == 'Jumia':
                    print(order.ordertype)
                    detailss = Order_Details.objects.create(
                                product=item, unit_price=item.jumia_unit_price, quantity=qty, gross_price=(item.jumia_unit_price * qty), order_id =order)
                else:
                    print(order.ordertype)
                    detailss = Order_Details.objects.create(
                                product=item, unit_price=item.unit_price, quantity=qty, gross_price=(item.unit_price * qty), order_id =order)


                gross_total = details.aggregate(cc=Sum('gross_price'))
                order.gross_price= gross_total['cc']
                order.save()

                messages.success(request, detailss.product.name +" " +"added successfully")
                return redirect('shop:tadd_items_to_charts',order.id)
    else:
        form = TakeOrderdetailsForm()

    template = 'backery/create_order_out.html'
    context ={
            "detail": details,
            "order": order,
            'form':form,


        }
    return render(request, template, context)

class Takeorderitems(CreateView):
    model = Order_Details
    form_class = TakeOrderdetailsForm
    template = 'backery/create_order_out.html'

    def get(self, *args, **kwargs):
        if self.request.session['id']:
            order_id = self.request.session['id']
            order = Order.objects.get(id=order_id)
            form = self.form_class()
            detail = Order_Details.objects.filter(order_id=order)
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
                order = Order.objects.get(id=order_id)
            if form.is_valid():

                instance = form.save(commit=False)
                product = Product.objects.get(name=instance.product)
                product_unit_price = product.unit_price
                instance.order_id = order
                instance.unit_price = product_unit_price
                instance.gross_price = product_unit_price * instance.quantity
                instance.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self, form):
        messages.success(self.request, 'Order item added')
        return super().form_valid(form)


@login_required
def makepayment(request,pk):
    order = Order.objects.get(id=pk)
    detail = Order_Details.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('shop:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount']
                order.save()

            #new start
            try:
                code= Sub_Accounts.objects.get(sub_code = 1202)
            except Sub_Accounts.DoesNotExist:
                pass
            try:
                jcode= Sub_Accounts.objects.get(sub_code = 1207)
            except Sub_Accounts.DoesNotExist:
                pass
            # new end
                # code = Account_code.objects.create(code="Sales")
            company = Company_group.objects.get(name="Party Tree Bakes")

            #new start
            try:
                cc=Account_Receivable.objects.get(bakes_order_no=order.id)
                cc.amount -= form.cleaned_data['amount']
                cc.save()
            except Account_Receivable.DoesNotExist:
                pass

            # sub_code = Sub_Accounts.objects.get(sub_code=1202)
            # General_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description='Payment of Bakes order with id'+ ' ' +str(order.id) ,debit=form.cleaned_data['amount_paid'])
            #new end
            v =form.cleaned_data['amount']
            shifts = UserShift.objects.all().order_by('id')
            shift = shifts.last()
            print(shift.id)

            if order.ordertype == 'Jumia':
                ARevenue.objects.create(
                account_code=jcode, amount=v, company=company,shift=shift,status='Jumia',close='New')
            else:
                ARevenue.objects.create(
                    account_code=code, amount=v, company=company,shift=shift,status='Cash',close='New')
            PaymentThread(order).start()

            messages.success(request, 'Payment made Sucessfully')
            return redirect('shop:manage_order')
    else:
        form = paymentForm()
    template = 'backery/check.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)


@login_required
def momomakepayment(request,pk):
    order = Order.objects.get(id=pk)
    detail = Order_Details.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('shop:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount']
                order.save()

            #new start
            try:
                code= Sub_Accounts.objects.get(sub_code = 1204)
            except Sub_Accounts.DoesNotExist:
                pass
            # new end
                # code = Account_code.objects.create(code="Sales")
            company = Company_group.objects.get(name="Party Tree Bakes")

            #new start
            try:
                cc=Account_Receivable.objects.get(bakes_order_no=order.id)
                cc.amount -= form.cleaned_data['amount']
                cc.save()
            except Account_Receivable.DoesNotExist:
                pass

            # sub_code = Sub_Accounts.objects.get(sub_code=1202)
            # General_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description='Payment of Bakes order with id'+ ' ' +str(order.id) ,debit=form.cleaned_data['amount_paid'])
            #new end
            v =form.cleaned_data['amount']
            shifts = UserShift.objects.all().order_by('id')
            shift = shifts.last()
            print(shift.id)
            ARevenue.objects.create(
                account_code=code, amount=v, company=company,shift=shift,status='Momo',close='New')
            PaymentThread(order).start()

            messages.success(request, 'Payment made Sucessfully')
            return redirect('shop:manage_order')
    else:
        form = paymentForm()
    template = 'backery/check.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)



@login_required
def debt(request):
    ord = Order.objects.filter(balance__gt=0.00)
    total = ord.aggregate(cc=Sum('total_price'))

    myFilter = AccountRecievableFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = myFilter.qs.aggregate(cc=Sum('total_price'))

    template = 'backery/accountrecieve.html'
    context = {
        'ord': ord,
        'myFilter': myFilter,
        'total': total,
    }
    return render(request, template, context)


def daily_saless(request):
    today = datetime.datetime.now()
    profile = request.user.profile
    company = Company_group.objects.get(name="Party Tree Bakes")
    ord = ARevenue.objects.filter(company=company.id,
        created_date=today,shift__profile=profile)
    total = ord.aggregate(cc=Sum('amount'))
    od = Order.objects.filter(order_date=today).count()
    template = 'backery/dailysaless.html'
    context = {
        'ord': ord,
        'total': total,
        'od': od,
    }
    return render(request, template, context)


def admin_order(request):
    today =datetime.date.today()
    orders = Order.objects.filter(gross_price__gt=0.00,)
    ord = Order.objects.filter(gross_price__gt=0.00,)
    company = Company_group.objects.get(name="Party Tree Bakes")
    to = ord.count()
    grss = ARevenue.objects.filter(company=company.id,status='Cash'
        ).aggregate(cc=Sum('amount'))
    momo = ARevenue.objects.filter(company=company.id,status='Momo').aggregate(bb=Sum('amount'))
    jumia = ARevenue.objects.filter(company=company.id,status='Jumia').aggregate(bb=Sum('amount'))
    total = ARevenue.objects.filter(company=company.id).aggregate(dd=Sum('amount'))


    orders = Order.objects.filter(clear=False,)
    template = 'backery/manage_orders.html'
    context = {
        'orders': orders,
        'to':to,
        'grss':grss,
        'momo':momo,
        'total':total,
        'jumia':jumia,
    }
    return render(request,template,context)