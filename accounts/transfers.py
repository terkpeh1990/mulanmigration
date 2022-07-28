from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *

def manage_transfer(request):
    payables = Transfers.objects.all()

    myFilter = TransferFilter(request.GET, queryset=payables)
    payables = myFilter.qs

    if request.method =='POST':
        form=transferform(request.POST)

        if form.is_valid():

            cc=form.save(commit=False)
            cc.status= 'Pending'
            cc.save()

            messages.success(request,"Transfer Initiated")
            return redirect('accounts:manage_transfer')
    else:
        form = transferform()

    template = 'accounts/manage_transfer.html'
    context={
        'payables':payables,
        'myFilter':myFilter,
        'form':form,
    }
    return render(request,template,context)


def edit_transfer(request,pk):
    transfer = Transfers.objects.get(id=pk)


    if request.method =='POST':
        form=transferform(request.POST,instance=transfer)

        if form.is_valid():

            form.save()

            messages.success(request,"Transfer Edited")
            return redirect('accounts:manage_transfer')
    else:
        form = transferform(instance=transfer)

    template = 'accounts/edit_transfer.html'

    context={

        'form':form,
    }
    return render(request,template,context)

def cancel_tranfer(request,pk):
    pv = Transfers.objects.get(id=pk)
    pv.status = "Cancelled"
    pv.save()
    messages.success(request,'Transfer Cancelled')
    return redirect('accounts:manage_transfer')


def comfirm_tranfer(request,pk):
    pv = Transfers.objects.get(id=pk)
    debit_transaction=General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.toaccount_code,description=pv.tran_dec,debit=pv.amount)
    credit_transaction=General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.fromaccount_code,description=pv.tran_dec,cedit=pv.amount)
    Bank_Cash_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.toaccount_code,description=pv.tran_dec,amount=pv.amount)
    Bank_Cash_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.fromaccount_code,description=pv.tran_dec,amount=(-pv.amount))
    pv.status = "Comfirmed"
    pv.save()
    messages.success(request,'Transfer Comfirmed')
    return redirect('accounts:manage_transfer')



