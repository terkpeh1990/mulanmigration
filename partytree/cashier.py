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
from school_management_system.settings import TWILIO_ACCOUNT_SID3, TWILIO_AUTH_TOKEN3, TWILIO_PHONE_NUMBER3
from twilio.rest import Client
from accounts.models import ARevenue,AExpenditure,Sub_Accounts,General_Ledger,Account_Receivable #new


@login_required
def create_order(request):
    order = Orders.objects.create()
    return redirect('partytree:add_items_to_chart', order.id)





def cancel_order(request,pk):
    order = Orders.objects.get(id=pk)
    details = Order_Detailss.objects.filter(order_id=order.id)
    for a in details:
        get_inventory = Inventorys.objects.get(product_id=a.product)
        get_inventory.outgoing -= a.quantity
        get_inventory.save()
    order.delete()
    messages.success(request,"Order Cancelled")
    return redirect('partytree:manage_order')


def add_items_to_chart(request,pk):


    order = Orders.objects.get(id=pk)
    try:
        details= Order_Detailss.objects.filter(order_id=order.id)
        gross_total = details.aggregate(cc=Sum('gross_price'))
        order.gross_price= gross_total['cc']
        order.save()
    except Order_Detailss.DoesNotExist:
        pass


    product = Products.objects.all()


    if request.method =='POST':
        form=OrderdetailsForm(request.POST)
        prod = request.POST.get("product")
        a,_,_= prod.split('-----')
        print(a)
        print(prod)


        if form.is_valid():
            qty = form.cleaned_data.get('quantity')

            item = Products.objects.get(id=a)
            if Order_Detailss.objects.filter(product=item,order_id=order).exists():
                messages.success(request, item.name+" "+"has already been selected")
                return redirect('partytree:add_items_to_chart',order.id)
            else:
                get_inventory = Inventorys.objects.get(product_id=item.id)
                print(get_inventory.avialable_stock)
                if get_inventory.avialable_stock < qty:
                    messages.success(request, "quantity Entered Cannot Be more than" + " "+ str(get_inventory.avialable_stock))
                    return redirect('partytree:add_items_to_chart',order.id)
                else:
                    detailss = Order_Detailss.objects.create(
                                 product=item, unit_price=item.unit_price, quantity=qty, gross_price=(item.unit_price * qty), order_id =order)
                    get_inventory.outgoing += qty
                    get_inventory.save()
                    gross_total = details.aggregate(cc=Sum('gross_price'))
                    order.gross_price= gross_total['cc']
                    order.save()

                messages.success(request, detailss.product.name +" " +"added successfully")
                return redirect('partytree:add_items_to_chart',order.id)
    else:
        form = OrderdetailsForm()

    template = 'partytree/create_order.html'
    context ={
            "detail": details,
            "order": order,
            'form':form,
            'product':product,

        }
    return render(request, template, context)



class orderitems(CreateView):
    model = Order_Details
    form_class = OrderdetailsForm
    template = 'partytree/create_order.html'

    def get(self, *args, **kwargs):
        if self.request.session['id']:
            order_id = self.request.session['id']
            order = Orders.objects.get(id=order_id)
            form = self.form_class()
            detail = Order_Detailss.objects.filter(order_id=order)
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
                order = Orders.objects.get(id=order_id)
            if form.is_valid():

                instance = form.save(commit=False)
                product = Products.objects.get(name=instance.product)
                product_unit_price = product.unit_price
                instance.order_id = order
                instance.unit_price = product_unit_price
                instance.gross_price = product_unit_price * instance.quantity
                instance.save()
                get_product = Inventorys.objects.get(product_id=product.id)
                get_product.instock -= instance.quantity
                get_product.outgoing += instance.quantity
                print(get_product.instock)
                get_product.save()
                Inventory_recordss.objects.create(
                    product=product, quantity=instance.quantity, unit_price=product.unit_price, status="Outgoing")
                # get_product.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self, form):
        messages.success(self.request, 'Sales item added')
        return super().form_valid(form)


@login_required
def deletes(request, pk):
    pro = Order_Detailss.objects.get(id=pk)
    order_id = pro.order_id
    product = Products.objects.get(name=pro.product)
    get_product = Inventorys.objects.get(product_id=product.id)
    get_product.outgoing -= pro.quantity
    get_product.save()
    Inventory_recordss.objects.create(
        product=product, quantity=pro.quantity, unit_price=product.unit_price, status="Incoming")
    pro.delete()
    messages.success(request, 'Item Removed')
    return redirect('partytree:add_items_to_chart',order_id )


@login_required
def checkout(request,pk):


    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('partytree:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount']
                order.save()


            try:
                code= Sub_Accounts.objects.get(sub_code=1202)
                # code = Account_code.objects.get(code="Sales")
            except Sub_Accounts.DoesNotExist:
                pass

            try:
                company = Company_group.objects.get(name="Party Tree")
            except Company_group.DoesNotExist:
                company = Company_group.objects.create(name="Party Tree")

            ARevenue.objects.create(
                account_code=code, amount=cc, company=company,status='Cash',close='New')
            # client = Client(TWILIO_ACCOUNT_SID3, TWILIO_AUTH_TOKEN3)
            # ,http_client=proxy_client
            today = datetime.datetime.now().date()

            # try:
            #     message = client.messages.create(
            #         to="+233" + order.customer.phone,
            #         from_=TWILIO_PHONE_NUMBER3,
            #         body="Dear" + " " + order.customer.name + "," + " " + "The total cost of your order with ID" + " "+order.id + " " + "is " + " " + "GHC" + " " + str(order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(order.amount_paid) + " " + ".Thank you for choosing Party Tree, For enquiries and orders, Please contact us on 0302941093 or 0209684691(Whatsapp).")
            # except IOError:
            #     print('fail')
            #     pass


    else:
        form = paymentForm()
    template = 'partytree/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)


@login_required
def momocheckout(request,pk):


    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('partytree:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount']
                order.save()


            try:
                code= Sub_Accounts.objects.get(sub_code=1202)
                # code = Account_code.objects.get(code="Sales")
            except Sub_Accounts.DoesNotExist:
                pass

            try:
                company = Company_group.objects.get(name="Party Tree")
            except Company_group.DoesNotExist:
                company = Company_group.objects.create(name="Party Tree")

            ARevenue.objects.create(
                account_code=code, amount=cc, company=company,status='Momo',close='New')
            # client = Client(TWILIO_ACCOUNT_SID3, TWILIO_AUTH_TOKEN3)
            # ,http_client=proxy_client
            today = datetime.datetime.now().date()

            # try:
            #     message = client.messages.create(
            #         to="+233" + order.customer.phone,
            #         from_=TWILIO_PHONE_NUMBER3,
            #         body="Dear" + " " + order.customer.name + "," + " " + "The total cost of your order with ID" + " "+order.id + " " + "is " + " " + "GHC" + " " + str(order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(order.amount_paid) + " " + ".Thank you for choosing Party Tree, For enquiries and orders, Please contact us on 0302941093 or 0209684691(Whatsapp).")
            # except IOError:
            #     print('fail')
            #     pass


    else:
        form = paymentForm()
    template = 'partytree/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)

@login_required
def checkout_print(request, pk):

    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)
    template = 'partytree/checkout_print.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


@login_required
def Vew_order(request, pk):

    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)
    template = 'partytree/view_order.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


@login_required
def close_order(request):
    #new
    return redirect('partytree:manage_order')
    #new end





@login_required
def close(request):
    return redirect('partytree:manage_order')


@login_required
def manage_order(request):
    today =datetime.date.today()
    list_inventory = Inventorys.objects.filter(avialable_stock__gt=0)
    orders = Orders.objects.filter(gross_price__gt=0.00,order_date=today)
    ord = Orders.objects.filter(gross_price__gt=0.00,order_date=today)
    company = Company_group.objects.get(name="Party Tree")
    to = ord.count()
    grss = ARevenue.objects.filter(company=company.id,status='Cash',
        created_date=today).aggregate(cc=Sum('amount'))
    momo = ARevenue.objects.filter(company=company.id,status='Momo',
        created_date=today).aggregate(cc=Sum('amount'))
    total = ARevenue.objects.filter(company=company.id,
        created_date=today).aggregate(cc=Sum('amount'))
    template = 'partytree/manage_orders.html'
    context = {
        'orders': orders,
        'grss':grss,
        'momo':momo,
        'total':total,
        'to':to,
        'list_inventory':list_inventory,
    }
    return render(request, template, context)

def search_order(request):
    today =datetime.date.today()

    orders = Orders.objects.filter(gross_price__gt=0.00)

    to = orders.count()
    grss = orders.aggregate(cc=Sum('gross_price'))
    template = 'partytree/search.html'
    context = {
        'orders': orders,
        'grss':grss,
        'to':to,
    }
    return render(request, template, context)


@login_required
def makepayment(request, pk):
    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('partytree:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount']
                order.save()


            try:
                company = Company_group.objects.get(name="Party Tree")
            except Company_group.DoesNotExist:
                company = Company_group.objects.create(name="Party Tree")



             #new start
            try:
                code= Sub_Accounts.objects.get(sub_code = 3001)
            except Sub_Accounts.DoesNotExist:
                pass
            # new end
                # code = Account_code.objects.create(code="Sales")
            company = Company_group.objects.get(name="Party Tree")

            #new start
            try:
                cc=Account_Receivable.objects.get(partytree_order_no=order.id)
                cc.amount -= form.cleaned_data['amount']
                cc.save()
            except Account_Receivable.DoesNotExist:
                pass

            # sub_code = Sub_Accounts.objects.get(sub_code=1202)
            # General_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description='Payment of Bakes order with id'+ ' ' +str(order.id) ,debit=form.cleaned_data['amount_paid'])
            #new end
            v =form.cleaned_data['amount']
            ARevenue.objects.create(
                account_code=code, amount=v, company=company,status='Cash',close='New')
            # try:
            #     message = client.messages.create(
            #         to="+233" + order.customer.phone,
            #         from_=TWILIO_PHONE_NUMBER3,
            #         body="Dear" + " " + order.customer.name + "," + " " + "The total cost of your order with ID" + " "+order.id + " " + "is " + " " + "GHC" + " " + str(order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(order.amount_paid) + " " + ".Thank you for choosing Party Tree, For enquiries and orders, Please contact us on 0302941093 or 0209684691(Whatsapp).")
            # except IOError:
            #     print('fail')
            #     pass

            messages.success(request, 'Payment made Sucessfully')
            return redirect('partytree:manage_order')
    else:
        form = paymentForm()
    template = 'partytree/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)


@login_required
def momomakepayment(request, pk):
    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('partytree:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount']
                order.save()


            try:
                company = Company_group.objects.get(name="Party Tree")
            except Company_group.DoesNotExist:
                company = Company_group.objects.create(name="Party Tree")



             #new start
            try:
                code= Sub_Accounts.objects.get(sub_code = 3001)
            except Sub_Accounts.DoesNotExist:
                pass
            # new end
                # code = Account_code.objects.create(code="Sales")
            company = Company_group.objects.get(name="Party Tree")

            #new start
            try:
                cc=Account_Receivable.objects.get(partytree_order_no=order.id)
                cc.amount -= form.cleaned_data['amount']
                cc.save()
            except Account_Receivable.DoesNotExist:
                pass

            # sub_code = Sub_Accounts.objects.get(sub_code=1202)
            # General_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description='Payment of Bakes order with id'+ ' ' +str(order.id) ,debit=form.cleaned_data['amount_paid'])
            #new end
            v =form.cleaned_data['amount']
            ARevenue.objects.create(
                account_code=code, amount=v, company=company,status='Momo',close='New')
            # try:
            #     message = client.messages.create(
            #         to="+233" + order.customer.phone,
            #         from_=TWILIO_PHONE_NUMBER3,
            #         body="Dear" + " " + order.customer.name + "," + " " + "The total cost of your order with ID" + " "+order.id + " " + "is " + " " + "GHC" + " " + str(order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(order.amount_paid) + " " + ".Thank you for choosing Party Tree, For enquiries and orders, Please contact us on 0302941093 or 0209684691(Whatsapp).")
            # except IOError:
            #     print('fail')
            #     pass

            messages.success(request, 'Payment made Sucessfully')
            return redirect('partytree:manage_order')
    else:
        form = paymentForm()
    template = 'partytree/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)




def daily_sales(request):
    today = datetime.datetime.now()
    company = Company_group.objects.get(name="Party Tree")
    ord = ARevenue.objects.filter(company=company.id,
        created_date=today)
    total = ord.aggregate(cc=Sum('amount'))
    od = Orders.objects.filter(order_date=today).count()
    template = 'partytree/dailysales.html'
    context = {
        'ord': ord,
        'total': total,
        'od': od,
    }
    return render(request, template, context)


def populate_inventory(request):
    inven = Inventorys.objects.all()
    for item in inven:
        item.instock = 400
        item.save()
    return redirect('partytree:manage_inventory')