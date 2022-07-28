from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def sub_accounts(request,pk):
    
    accounts = Accounts.objects.get(id=pk)
    sub_accounts=Sub_Accounts.objects.filter(code=pk)
    total_sub_accounts = sub_accounts.count()
    last_sub_accounts_code = sub_accounts.last()
    
    if request.method == 'POST':
        form = SubAccountsForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.code = accounts
            cc.save()
            messages.success(request,'Account Saved')
            return redirect('accounts:sub_accounts',pk=accounts.id)
    
    else:
        form = SubAccountsForm()

    template = 'accounts/sub_accounts.html'

    context = {
        'accounts': accounts,
        'total_sub_accounts':total_sub_accounts,
        'last_sub_accounts_code':last_sub_accounts_code,
        'form':form,
        'sub_accounts':sub_accounts,
    }

    return render(request,template,context)


def edit_sub_accounts(request,pk):
    
    
    sub_account = Sub_Accounts.objects.get(id=pk)
    print(sub_account.code)
    accounts = Accounts.objects.get(id=sub_account.code.id)
    print(accounts.id)
    sub_accounts=Sub_Accounts.objects.filter(code=accounts.id)
   
    total_sub_accounts = sub_accounts.count()
    last_sub_accounts_code = sub_accounts.last()
    
    if request.method == 'POST':
        form = SubAccountsForm(request.POST,instance=sub_account)
        if form.is_valid():
            form.save()
            messages.success(request,'Sub Accounts Updated')
            return redirect('accounts:sub_accounts',accounts.id)
    
    else:
        form = SubAccountsForm(instance=sub_account)

    template = 'accounts/sub_accounts.html'

    context = {
        'accounts': accounts,
        'total_sub_accounts':total_sub_accounts,
        'last_sub_accounts_code':last_sub_accounts_code,
        'form':form,
        'sub_accounts':sub_accounts,
        'sub_account':sub_account,
        'accounts':accounts,
    }

    return render(request,template,context)