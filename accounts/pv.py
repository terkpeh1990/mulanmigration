from re import template
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *

def create_pv(request):
    if request.method == "POST":
        form = PvForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.status = "Pending"
            cc.save()
            return redirect('accounts:pv_detail',cc.id)
    else:
        form = PvForm()
    template = 'accounts/create_pv.html'
    context = {
        'form':form,
    }
    return render(request,template,context)


def pv_detail(request,pk):
    
    pv = Payment_Vouchers.objects.get(id=pk)
    form = Pv_detailsForm()
    detail = APv_details.objects.filter(payment_voucher=pv.id)
    if detail:
        gross_total = detail.aggregate(cc=Sum('amount'))
        pv.amount = gross_total['cc']
        pv.save()
    else:
        gross_total = 0.00
        pv.amount = gross_total
        pv.save()
   

    if request.method =='POST':
        form = Pv_detailsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.payment_voucher = pv 
            # tt= form.aggregate(cc=Sum('amount'))
            cc= form.save()
            # pv.amount +=cc.amount
            pv.save()
            messages.success(request, 'Pv item added')
            return redirect('accounts:pv_detail',pv.id)

    template = 'accounts/pv_details.html'
    context ={
        'pv':pv,
        'detail':detail,
        'gross_total':gross_total,
        'form':form,
    }
    return render(request, template, context)



def deletes_pvitems(request,pk):
    pro = APv_details.objects.get(id=pk)
    pv = Payment_Vouchers.objects.get(id=pro.payment_voucher.id)
    pv.amount -=pro.amount
    pv.save()
    pro.delete()
    return redirect('accounts:pv_detail',pv.id)



def manage_pv(request):
    pv = Payment_Vouchers.objects.all()
    template = 'accounts/manage_pv.html'
    context={
        'pv':pv,
    }
    return render(request,template,context)

def pending_pv(request):
    pv = Payment_Vouchers.objects.filter(status = "Pending")
    template = 'accounts/manage_pv.html'
    context={
        'pv':pv,
    }
    return render(request,template,context)

def view_pv(request,pk):
    
    order = Payment_Vouchers.objects.get(id=pk)
    detail = APv_details.objects.filter(payment_voucher=order.id)
    template = 'accounts/view_pv.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


def cancelled(request,pk):
    pv = Payment_Vouchers.objects.get(id=pk)
    pv.status = "cancelled"
    pv.save()
    messages.success(request,'PV Cancelled')
    return redirect('accounts:pending_pv')

def approve(request,pk):
    pv = Payment_Vouchers.objects.get(id=pk)
    pv.status = "approved"
    Account_Payables.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_account,description=pv.description,amount=pv.amount,reference=pv)
    General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_account,description=pv.description,debit=pv.amount)
    
  
    AExpenditure.objects.create(account_code=pv.sub_account,amount=pv.amount,company=pv.company,pvno=pv)
    pv.save()
    messages.success(request,'PV Approved')
    return redirect('accounts:pending_pv')



def void_pv(request,pk):
    pv = Payment_Vouchers.objects.get(id=pk)
    pv.status = "void"
    pv.save()
    payables = Account_Payables.objects.get(reference=pv.id)
    General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_account,description=pv.description + " "+ "has been made void" ,cedit=payables.amount)
    exp =AExpenditure.objects.get(pvno=pv.id)
    exp.amount-= payables.amount
    payables.amount = 0.00
    payables.save()
    
    messages.success(request,'PV Voided')
    return redirect('accounts:manage_pv')




