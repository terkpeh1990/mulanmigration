from cProfile import Profile
from itertools import product
from tempfile import template
from unicodedata import category

from django.template import context
from .models import *
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from accounts.models import Account_Receivable, General_Ledger, Payment_Vouchers, Sub_Accounts,Bank_Cash_Ledger,AExpenditure,APv_details,ARevenue #new
from school.models import Company_group
from django.db.models import Sum
from .filters import ReportFilter
from django.db.models.functions import TruncMonth


def manage_shift(request):
    shifts = UserShift.objects.filter(status_checking=True)
    template_name = 'bakeryshift/shift.html'

    context = {
        'shifts':shifts
    }
    return render(request,template_name,context)

def user_shift(request):
    profile = request.user.profile
    shifts = UserShift.objects.filter(profile=profile,status_checking=True)
    template_name = 'bakeryshift/shift.html'

    context = {
        'shifts':shifts
    }
    return render(request,template_name,context)


def create_shift(request):

    try:
        bb = UserShift.objects.all().order_by('id')
        cc = bb.last()
        # print(cc.id)
        # print(cc.starttime)
        if cc is None:
            try:
                shift = Shift.objects.get(name ='Morning')
            except Shift.DoesNotExist:
                shift = Shift.objects.create(name ='Morning')
            profile = request.user.profile
            today = datetime.datetime.now()
            UserShift.objects.create(profile=profile,shift=shift, starttime=today,status='Open')
            messages.success(request,"Your shift is opened. Please remember to close your shift is over")
            return redirect('shop:manage_shift')
        elif cc.endtime is None:
            messages.success(request,"Please Close Previous Shift")
            return redirect('shop:manage_shift')
        else:
            profile = request.user.profile
            if cc.shift.name == 'Morning':
                try:
                    shift = Shift.objects.get(name ='Afternoon')
                except Shift.DoesNotExist:
                    shift = Shift.objects.create(name ='Afternoon')
            else:
                shift = Shift.objects.get(name ='Morning')
            today = datetime.datetime.now()
            usershif=UserShift.objects.create(profile=profile,shift=shift, starttime=today,status='Open')
            today = datetime.datetime.now()

            inventorys = Inventory.objects.all()

            #new Start
            stock = inventorys.aggregate(bb=Sum('avialable_stock'))
            stock_value =inventorys.aggregate(cc =Sum('avialable_stock_cost'))

            close_stock=BOpening_Stock_summery.objects.create(stock=stock['bb'],usershift=usershif,closing_stock_value=stock_value['cc'])
            for inventory in inventorys:
                product = Product.objects.get(id=inventory.product_id.id)
                print(product)
                Opening_stocks.objects.create(
                    product=product, closing_stock=inventory.avialable_stock,open_stock_summery=close_stock ,avialable_stock_cost=inventory.avialable_stock_cost)
            messages.success(request,"Your shift is opened. Please remember to close your shift is over")
            return redirect('shop:manage_shift')
    except UserShift.DoesNotExist:
        usershif=UserShift.objects.create(profile=profile,shift=shift, starttime=today,status='Open')
        stock = inventorys.aggregate(bb=Sum('avialable_stock'))
        stock_value =inventorys.aggregate(cc =Sum('avialable_stock_cost'))

        close_stock=BOpening_Stock_summery.objects.create(stock=stock['bb'],usershift=usershif,closing_stock_value=stock_value['cc'])
        for inventory in inventorys:
            product = Product.objects.get(id=inventory.product_id.id)
            print(product)
            Opening_stocks.objects.create(
                product=product, closing_stock=inventory.avialable_stock,open_stock_summery=close_stock ,avialable_stock_cost=inventory.avialable_stock_cost)
        messages.success(request,"Your shift is opened. Please remember to close your shift is over")
        return redirect('shop:manage_shift')


def close_shift (request,pk):
    shift = UserShift.objects.get(id=pk)
    today = datetime.datetime.now()
    today =datetime.date.today()
    inventorys = Inventory.objects.all()

    #new Start
    stock = inventorys.aggregate(bb=Sum('avialable_stock'))
    stock_value =inventorys.aggregate(cc =Sum('avialable_stock_cost'))

    close_stock=BClosing_Stock_summery.objects.create(stock=stock['bb'],usershift=shift,closing_stock_value=stock_value['cc'])
    for inventory in inventorys:
        product = Product.objects.get(id=inventory.product_id.id)
        print(product)
        Closing_stocks.objects.create(
            product=product, closing_stock=inventory.avialable_stock,stock_summery=close_stock ,avialable_stock_cost=inventory.avialable_stock_cost)

    order = Order.objects.filter(order_date = today, balance__gt=0.00,usershift__profile = request.user.profile)
    company = Company_group.objects.get(name="Party Tree Bakes")

    code= Sub_Accounts.objects.get(sub_code = 3001)
    dcode= Sub_Accounts.objects.get(sub_code=1202)
    momo_code = Sub_Accounts.objects.get(sub_code=1204)
    jumia_code = Sub_Accounts.objects.get(sub_code=1207)

    rev = ARevenue.objects.filter(company=company,close='New', shift__profile=request.user.profile)
    sales = rev.aggregate(cc =Sum('amount'))

    ca = rev.filter(status='Cash')
    mo = rev.filter(status='Momo')
    jumia = rev.filter(status='Jumia')
    if ca:
        cash = ca.aggregate(cc =Sum('amount'))
        General_Ledger.objects.create(transaction_date=today,sub_code=dcode,description='Sales From Partytree Bakes',debit=cash['cc'])
        Bank_Cash_Ledger.objects.create(transaction_date=today,sub_code=dcode,description='Sales From Partytree Bakes',amount=cash['cc'])

    if mo:
        momo = mo.aggregate(cc =Sum('amount'))
        General_Ledger.objects.create(transaction_date=today,sub_code=momo_code,description='Sales From Partytree Bakes',debit=momo['cc'])
        Bank_Cash_Ledger.objects.create(transaction_date=today,sub_code=momo_code,description='Sales From Partytree Bakes',amount=momo['cc'])

    if jumia:
        jumia = jumia.aggregate(cc =Sum('amount'))
        General_Ledger.objects.create(transaction_date=today,sub_code=jumia_code,description='Jumia Sales From Partytree Bakes',debit=jumia['cc'])
        Bank_Cash_Ledger.objects.create(transaction_date=today,sub_code=jumia_code,description='Jumia Sales From Partytree Bakes',amount=jumia['cc'])

    if sales['cc'] is not None:
        print(sales)
        General_Ledger.objects.create(transaction_date=today,sub_code=code,description='Sales From Partytree Bakes',cedit=sales['cc'],)

    for i in rev:
        i.close='Old'
        i.save()

    for a in order:
        Account_Receivable.objects.create(transaction_date=today,sub_code=code,description='PartyTree Bakes order not paid',amount=a.balance,bakes_order_no=a)
    if order:
        for a in order:
            Account_Receivable.objects.create(transaction_date=today,sub_code=code,description='PartyTree Bakes order not paid',amount=a.balance,bakes_order_no=a)
        if order:
            bb = order.aggregate(vv =Sum('balance'))
            General_Ledger.objects.create(transaction_date=today,sub_code=code,description='PartyTree Bakes order not paid',cedit=bb['vv'])
        else:
            bb = 0.00
            General_Ledger.objects.create(transaction_date=today,sub_code=code,description='PartyTree Bakes order not paid',cedit=0.00)



    shift.status = 'Closed'
    shift.endtime = today
    shift.save()
    messages.success(request, "Shift Closed")
    return redirect('shop:manage_shift')


def view_shift(request,pk):
    shift = UserShift.objects.get(id=pk)
    try:
        shift_close_stock_summery = BClosing_Stock_summery.objects.get(usershift=shift.id)
    except BClosing_Stock_summery.DoesNotExist:
        shift_close_stock_summery = 0
    try:
        shift_open_stock_summery = BOpening_Stock_summery.objects.get(usershift=shift)
    except BOpening_Stock_summery.DoesNotExist:
        shift_open_stock_summery = 0
    revenue_list = ARevenue.objects.filter(shift=shift.id)
    sales = revenue_list.aggregate(cc =Sum('amount'))
    orders = Order.objects.filter(gross_price__gt=0.00,usershift= shift.id)
    total_orders = orders.count()
    cash_sales = revenue_list.filter(status='Cash').aggregate(cc=Sum('amount'))
    momo_sales = revenue_list.filter(status='Momo').aggregate(cc=Sum('amount'))
    jumia_sales = revenue_list.filter(status='Jumia').aggregate(cc=Sum('amount'))


    tempplate_name = 'bakeryshift/view_shift.html'
    context ={
        'shift_close_stock_summery':shift_close_stock_summery,
        'shift_open_stock_summery':shift_open_stock_summery,
        'revenue_list':revenue_list,
        'sales':sales,
        'orders':orders,
        'total_orders':total_orders,
        'cash_sales':cash_sales,
        'momo_sales':momo_sales,
        'jumia_sales':jumia_sales,
        'shift':shift,

    }
    return render(request,tempplate_name,context )



def view_closing_stock(request,pk):
    close_stock = Closing_stocks.objects.filter(stock_summery=pk)
    template_name = 'backery/closedstock.html'

    context = {
        'close_stock':close_stock
    }
    return render(request,template_name,context)

def view_opening_stock(request,pk):
    close_stock = Opening_stocks.objects.filter(open_stock_summery=pk)
    template_name = 'backery/closedstock.html'

    context = {
        'close_stock':close_stock
    }
    return render(request,template_name,context)




def view_report(request,pk):
    order = Order_Details.objects.filter(product__category=pk)
    total = order.count()
    total_value = order.aggregate(cc=Sum('gross_price'))

    myFilter = ReportFilter(request.GET, queryset=order)
    order = myFilter.qs
    total = order.count()
    total_value = order.aggregate(cc=Sum('gross_price'))


    template_name = 'bakeryshift/report.html'
    context ={
        'order':order,
        'total':total,
        'total_value':total_value,
        'myFilter':myFilter,


    }
    return render(request,template_name,context)

def view_yearly_report(request,pk):
    order = Order_Details.objects.filter(product__category=pk)
    table = order.annotate(month = TruncMonth('order_id__order_date'))
    rep =table.values('month').annotate(total_orders=Count('id'), total_quantity=Sum('quantity'), total_value=Sum('gross_price'),).values('month','total_orders','total_quantity','total_value').order_by('month')
    total = order.aggregate(cc=Sum('quantity'))
    total_value = order.aggregate(cc=Sum('gross_price'))

    myFilter = ReportFilter(request.GET, queryset=order)
    order = myFilter.qs
    table = order.annotate(month = TruncMonth('order_id__order_date'))
    rep =table.values('month').annotate(total_orders=Count('id'), total_quantity=Sum('quantity'), total_value=Sum('gross_price'),).values('month','total_orders','total_quantity','total_value').order_by('month')
    total = order.aggregate(cc=Sum('quantity'))
    total_value = order.aggregate(cc=Sum('gross_price'))

    template_name = 'bakeryshift/yearly_stats.html'
    context ={
        'total':total,
        'total_value':total_value,
        'rep':rep,
        'myFilter':myFilter,


    }
    return render(request,template_name,context)

def view_product_report(request,pk):
    order = Order_Details.objects.filter(product__category=pk)
    last = order.last()
    kk=True
    aa=last.product.category.id
    bb = Product.objects.filter(category = aa)
    for i in bb:
        print(i.name  ,i.category.name)
    rep =bb.values('name').annotate(total_orders=Count('order_details__id'), total_quantity=Sum('order_details__quantity'), total_value=Sum('order_details__gross_price'),).values('name','total_orders','total_quantity','total_value').order_by('total_value')

    total = order.aggregate(cc=Sum('quantity'))
    total_value = order.aggregate(cc=Sum('gross_price'))

    myFilter = ReportFilter(request.GET, queryset= order)
    order = myFilter.qs
    if order:
        last = order.last()
        aa=last.product.category.id
        bb = Product.objects.filter(category = aa)
        rep =bb.values('name').annotate(total_orders=Count('order_details__id'), total_quantity=Sum('order_details__quantity'), total_value=Sum('order_details__gross_price'),).values('name','total_orders','total_quantity','total_value').order_by('total_value')
        total = order.aggregate(cc=Sum('quantity'))
        total_value = order.aggregate(cc=Sum('gross_price'))
    else:
        kk=False



    template_name = 'bakeryshift/productstats.html'
    context ={
        'total':total,
        'total_value':total_value,
        'rep':rep,
        'myFilter':myFilter,
        'kk':kk,


    }
    return render(request,template_name,context)



def view_yearly_product_report(request,pk):
    order = Order_Details.objects.filter(product=pk)
    table = order.annotate(month = TruncMonth('order_id__order_date'))
    rep =table.values('month').annotate(total_orders=Count('id'), total_quantity=Sum('quantity'), total_value=Sum('gross_price'),).values('month','total_orders','total_quantity','total_value').order_by('month')
    total = order.aggregate(cc=Sum('quantity'))
    total_value = order.aggregate(cc=Sum('gross_price'))

    myFilter = ReportFilter(request.GET, queryset=order)
    order = myFilter.qs
    table = order.annotate(month = TruncMonth('order_id__order_date'))
    rep =table.values('month').annotate(total_orders=Count('id'), total_quantity=Sum('quantity'), total_value=Sum('gross_price'),).values('month','total_orders','total_quantity','total_value').order_by('month')
    total = order.aggregate(cc=Sum('quantity'))
    total_value = order.aggregate(cc=Sum('gross_price'))

    template_name = 'bakeryshift/yearly_stats.html'
    context ={
        'total':total,
        'total_value':total_value,
        'rep':rep,
        'myFilter':myFilter,


    }
    return render(request,template_name,context)



