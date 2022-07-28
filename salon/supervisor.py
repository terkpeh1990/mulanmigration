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
from school_management_system.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER2
from twilio.rest import Client
from .filters import *


# @login_required
def manage_category(request):
    category = SalonCategory.objects.all()

    template = 'salon/manage_category.html'

    context = {
        'category': category,
    }

    return render(request, template, context)


# @login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Created')
            return redirect('salon:manage_category')

    else:
        form = CategoryForm()

    template = 'salon/create_category.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# @login_required
def edit_category(request, pk):
    category = SalonCategory.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated')
            return redirect('salon:manage_category')

    else:
        form = CategoryForm(instance=category)

    template = 'salon/create_category.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# @login_required
def manage_product(request):
    product = SalonProduct.objects.all()

    template = 'salon/manage_product.html'

    context = {
        'product': product,
    }

    return render(request, template, context)


# @login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Created')
            return redirect('salon:manage_product')

    else:
        form = ProductForm()

    template = 'salon/create_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# @login_required
def edit_product(request, pk):
    product = SalonProduct.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Updated')
            return redirect('salon:manage_product')

    else:
        form = ProductForm(instance=product)

    template = 'salon/create_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# @login_required
def create_restock(request):
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            restockform = form.save(commit=False)
            restockform.status = "Incoming"
            product = Product.objects.get(id=restockform.product.id)
            restockform.unit_price = product.unit_price
            restockform.approval = "Pending"
            restockform.save()
            messages.success(request, 'Restock Created Waiting For Approval')
            return redirect('salon:manage_restock')

    else:
        form = RestockForm()

    template = 'salon/restock.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def cancel_restock(request, pk):
    restock = SalonInventory_records.objects.get(pk=pk)
    restock.approval = "Cancelled"
    restock.save()
    messages.success(request, 'Restock Cancelled')
    return redirect('salon:pending_restock')


def approve_restock(request, pk):
    restock = SalonInventory_records.objects.get(pk=pk)
    try:
        product = SalonProduct.objects.get(id=restock.product.id)
        get_product = SalonInventory.objects.get(product_id=product.id)
        get_product.instock += restock.quantity
        get_product.unit_price = product.unit_price
        get_product.save()

    except SalonInventory.DoesNotExist:
        product = SalonProduct.objects.get(id=restock.product.id)
        SalonInventory.objects.create(
            product_id=product, instock=restock.quantity, unit_price=product.unit_price)
    restock.approval = "Approved"
    restock.save()
    messages.success(request, 'Restock Approved')
    return redirect('salon:pending_restock')


# @login_required
def manage_restock(request):
    restock = SalonInventory_records.objects.all()

    template = 'salon/manage_restock.html'

    context = {
        'restock': restock,
    }

    return render(request, template, context)


def pending_restock(request):
    restock = SalonInventory_records.objects.filter(approval='Pending')

    template = 'salon/manage_restock.html'

    context = {
        'restock': restock,
    }

    return render(request, template, context)


# @login_required
def manage_inventory(request):
    inventory = SalonInventory.objects.all()

    template = 'salon/manage_inventory.html'

    context = {
        'inventory': inventory,
    }

    return render(request, template, context)


# @login_required
def closing_stock(request):
    inventorys = SalonInventory.objects.all()
    for inventory in inventorys:
        product = SalonProduct.objects.get(id=inventory.product_id.id)
        SalonClosing_stocks.objects.create(
            product=product, closing_stock=inventory.avialable_stock, avialable_stock_cost=inventory.avialable_stock_cost, close_status="Approved")
    messages.success(request, 'Stock Closed')
    return redirect('salon:manage_inventory')



def closed_stock(request):
    close_stock = SalonClosing_stocks.objects.all().order_by('-id')
    template = 'salon/closedstock.html'

    context = {
        'close_stock': close_stock,
    }
    return render(request, template, context)


def daily_sales(request):
    today = datetime.datetime.now()
    company = Company_group.objects.get(name="Irish Green")
    ord = Revenue.objects.filter(company=company.id,
                                 created_date=today)
    total = ord.aggregate(cc=Sum('amount'))
    template = 'salon/revenueall.html'
    context = {
        'ord': ord,
        'total': total,
    }
    return render(request, template, context)


def taxation(request):
    ord = SalonOrder.objects.filter(vat__gt=0.00)
    total = ord.aggregate(cc=Sum('vat'))

    myFilter = AccountRecievableFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = myFilter.qs.aggregate(cc=Sum('vat'))

    template = 'salon/bakeryvat.html'
    context = {
        'ord': ord,
        'myFilter': myFilter,
        'total': total,
    }
    return render(request, template, context)

def EditInventory(request, pk):
    product_inventory = SalonInventory.objects.get(pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            product_inventory.outgoing += int(qty)
            product_inventory.save()
            messages.success(request, "Inventory Updated")
            return redirect('partytree:EditInventory', pk=product_inventory.id)
    else:
        form = InventoryForm()
    template = 'salon/updateinventory.html'
    context = {
        'form': form,
        'product_inventory': product_inventory
    }
    return render(request, template, context)

