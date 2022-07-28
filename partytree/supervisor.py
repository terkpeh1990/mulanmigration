from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from .forms import *
from .models import *
from school.models import *
from django.contrib.auth.decorators import login_required
import datetime
from accounts.models import Account_Receivable, General_Ledger, Payment_Vouchers, Sub_Accounts,Bank_Cash_Ledger,AExpenditure,APv_details,ARevenue #new
# from .filters import *


@login_required
def manage_category(request):
    category = Categorys.objects.all()

    template = 'partytree/manage_category.html'

    context = {
        'category': category,
    }

    return render(request, template, context)


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('partytree:manage_category')

    else:
        form = CategoryForm()

    template = 'partytree/create_category.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_category(request, pk):
    category = Categorys.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('partytree:manage_category')

    else:
        form = CategoryForm(instance=category)

    template = 'partytree/create_category.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# @login_required
def manage_product(request):
    product = Products.objects.all().order_by('name')

    template = 'partytree/manage_product.html'

    context = {
        'product': product,
    }

    return render(request, template, context)


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('partytree:manage_product')

    else:
        form = ProductForm()

    template = 'partytree/create_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, pk):
    product = Products.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('partytree:manage_product')

    else:
        form = ProductForm(instance=product)

    template = 'partytree/create_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def create_restock(request,pk):
    product = Products.objects.get(id=pk)
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cc=Inventory_recordss.objects.create(product=product,unit_price=product.unit_price,quantity=quantity,status="Incoming")


            try:
                product = Products.objects.get(id=pk)
                get_product = Inventorys.objects.get(product_id=product.id)
                get_product.instock += cc.quantity
                get_product.unit_price = product.unit_price
                get_product.save()

            except Inventorys.DoesNotExist:
                product = Products.objects.get(id=pk)
                Inventorys.objects.create(
                    product_id=product, instock=cc.quantity, unit_price=product.unit_price)

            messages.success(request,str(cc.quantity)+' '+ cc.product.name +' '+ 'added to Inventoey')

            return redirect('partytree:manage_product')

    else:
        form = RestockForm()

    template = 'partytree/restock.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def manage_restock(request):
    restock = Inventory_recordss.objects.all()

    template = 'partytree/manage_restock.html'

    context = {
        'restock': restock,
    }

    return render(request, template, context)


@login_required
def manage_damages(request):
    damage = Damagess.objects.all()

    template = 'partytree/manage_damages.html'

    context = {
        'damage': damage,
    }

    return render(request, template, context)


@login_required
def pending_damages(request):
    damage = Damagess.objects.filter(dastatus = "Pending")

    template = 'partytree/manage_damages.html'

    context = {
        'damage': damage,
    }

    return render(request, template, context)

@login_required
def create_damage(request,pk):
    product = Products.objects.get(id=pk)
    if request.method == 'POST':
        form = DamageForm(request.POST)
        if form.is_valid():
            quantity=form.cleaned_data['quantity']
            cause = form.cleaned_data['cause']

            Damagess.objects.create(product_id=product,quantity=quantity,cause =cause,dastatus="Pending")

            messages.success(request, 'Damage Recorded Waiting For Approval')
            return redirect('partytree:manage_damages')

    else:
        form = DamageForm()

    template = 'partytree/damages.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def manage_inventory(request):
    today =datetime.date.today()#new
    openings = Opening_Stock_summery.objects.last()
    closings = Closing_Stock_summery.objects.last()
    inventory = Inventorys.objects.all()
    # if openings:
    #     a = openings.close_date = today
    # else:
    #     pass
    # if closings:
    #     b = closings.close_date < today
    # else:
    #     pass
    template = 'partytree/manage_inventory.html'

    context = {
        'inventory': inventory,
        'openings':openings,
        'closings':closings,
        # 'a':a,
        # 'b':b,
    }

    return render(request, template, context)


@login_required
def closing_stock(request):
    today =datetime.date.today() # new
    inventorys = Inventorys.objects.all()


    #new Start
    stock = inventorys.aggregate(bb=Sum('avialable_stock'))
    stock_value =inventorys.aggregate(cc =Sum('avialable_stock_cost'))
    if Closing_Stock_summery.objects.filter(stock=stock['bb'],closing_stock_value=stock_value['cc']).exists():
        messages.success(request, 'Stock Already Closed')
        return redirect('partytree:manage_inventory')
    else:
        for inventory in inventorys:
            product = Products.objects.get(id=inventory.product_id.id)
        print(product)
        Closing_stockss.objects.create(
            product=product, closing_stock=inventory.avialable_stock, avialable_stock_cost=inventory.avialable_stock_cost)
        Closing_Stock_summery.objects.create(stock=stock['bb'],closing_stock_value=stock_value['cc'])
        order = Orders.objects.filter(order_date = today, balance__gt=0.00)
        company = Company_group.objects.get(name="Party Tree")
        rev = ARevenue.objects.filter(company=company,close='New')
        code= Sub_Accounts.objects.get(sub_code = 3001)
        dcode= Sub_Accounts.objects.get(sub_code=1202)
        momo_code = Sub_Accounts.objects.get(sub_code=1204)
        if rev:
            sales = rev.aggregate(cc =Sum('amount'))
            ca = rev.filter(status='Cash')
            mo = rev.filter(status='Momo')
            if ca:
                cash = ca.aggregate(cc =Sum('amount'))
                General_Ledger.objects.create(transaction_date=today,sub_code=dcode,description='Sales From Partytree',debit=cash['cc'])
                Bank_Cash_Ledger.objects.create(transaction_date=today,sub_code=dcode,description='Sales From Partytree',amount=cash['cc'])

            if mo:
                momo = mo.aggregate(cc =Sum('amount'))
                General_Ledger.objects.create(transaction_date=today,sub_code=momo_code,description='Sales From Partytree',debit=momo['cc'])
                Bank_Cash_Ledger.objects.create(transaction_date=today,sub_code=momo_code,description='Sales From Partytree',amount=momo['cc'])


            General_Ledger.objects.create(transaction_date=today,sub_code=code,description='Sales From Partytree',cedit=sales['cc'])

            for i in rev:
                i.close='Old'
                i.save()

            for a in order:
                Account_Receivable.objects.create(transaction_date=today,sub_code=code,description='Party Tree order not paid',amount=a.balance,partytree_order_no=a)
            if order:
                for a in order:
                    Account_Receivable.objects.create(transaction_date=today,sub_code=code,description='Party Tree order not paid',amount=a.balance,partytree_order_no=a)
                if order:
                    bb = order.aggregate(vv =Sum('balance'))
                    General_Ledger.objects.create(transaction_date=today,sub_code=code,description='Party Tree order not paid',cedit=bb['vv'])
                else:
                    bb = 0.00
                    General_Ledger.objects.create(transaction_date=today,sub_code=code,description='Party Tree order not paid',cedit=0.00)


    # new end

    messages.success(request, 'Stock Closed')
    return redirect('partytree:manage_inventory')


@login_required
def closed_stock(request):
    close_stock = Closing_stockss.objects.all().order_by('-id')
    template = 'partytree/closedstock.html'

    context = {
        'close_stock': close_stock,
    }
    return render(request, template, context)

def EditInventory(request, pk):
    product_inventory = Inventorys.objects.get(pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            product_inventory.instock -= int(qty)
            product_inventory.save()
            messages.success(request, "Inventory Updated")
            return redirect('partytree:EditInventory', pk=product_inventory.id)
    else:
        form = InventoryForm()
    template = 'partytree/updateinventory.html'
    context = {
        'form': form,
        'product_inventory': product_inventory
    }
    return render(request, template, context)

def run_to_zero(request):
    cc = Inventorys.objects.all()
    for i in cc:
        i.instock = 0
        i.outgoing = 0
        i.save()
    messages.success(request,"Run to Zero Done")
    return redirect('partytree:manage_inventory')



@login_required
def cancel_damages(request, pk):
    damage = Damagess.objects.get(pk=pk)
    damage.dastatus = "Cancelled"
    damage.save()
    messages.success(request, 'Damages Cancelled')
    return redirect('partytree:pending_damages')

@login_required
def approve_damage(request,pk):
    damage = Damagess.objects.get(pk=pk)
    today = datetime.datetime.now()
    try:
        product = Products.objects.get(id=damage.product_id.id)
        get_product = Inventorys.objects.get(product_id=product.id)
        get_product.outgoing += damage.quantity
        get_product.save()
        cost = product.unit_price * damage.quantity
        Inventory_recordss.objects.create(
            product=product, quantity=damage.quantity, unit_price=product.unit_price, status="Outgoing")
        try:
            sub_code = Sub_Accounts.objects.get(sub_code=1202)
        except Sub_Accounts.DoesNotExist:
            pass
        try:
            dsub_code = Sub_Accounts.objects.get(sub_code=4146)
        except Sub_Accounts.DoesNotExist:
            dsub_code=Sub_Accounts.objects.create(sub_code=4146,sub_description='DAMAGES')
        company = Company_group.objects.get(name="Party Tree")
        pv = Payment_Vouchers.objects.create(
                    sub_account=dsub_code, company=company, description="Cost of Damages From Party Tree", amount=cost, status="approved")
        pv_detail = APv_details.objects.create(
                    payment_voucher=pv, description=pv.description, amount=pv.amount)

        General_Ledger.objects.create(transaction_date=today,sub_code=dsub_code,description='Damage from Party Tree' ,debit=cost)
        General_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description='Damage from Party Tree' ,cedit=cost)
        Bank_Cash_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description='Damage from Party Tree' ,amount=(-cost))
        AExpenditure.objects.create(
                account_code=dsub_code, amount=cost, company=company)


    except Inventory.DoesNotExist:
        pass
    damage.dastatus = "Approved"
    damage.save()
    messages.success(request,'Damages Proccessed Successfully')
    return redirect('partytree:pending_damages')


#new start
@login_required
def open_stock(request):
    today =datetime.date.today() # new
    inventorys = Inventorys.objects.all()

    #new Start
    stock = inventorys.aggregate(bb=Sum('avialable_stock'))
    stock_value =inventorys.aggregate(cc =Sum('avialable_stock_cost'))
    Opening_Stock_summery.objects.create(stock=stock['bb'],closing_stock_value=stock_value['cc'])
    # new end

    messages.success(request, 'Stock Opened')
    return redirect('partytree:manage_inventory')



def pmanage_closingstock_summery(request):

    inventory = Closing_Stock_summery.objects.all()

    template = 'backery/closingstock_sum.html'

    context = {

        'inventory': inventory,
    }

    return render(request, template, context)

#new end