from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def manage_accounts(request):

    
    accounts = Accounts.objects.all()
    total_accounts = accounts.count()
    sub_accounts=Sub_Accounts.objects.all()
    total_sub_accounts = sub_accounts.count()
    last_accounts_code = accounts.last()
    
    if request.method == 'POST':
        form = AccountsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Saved')
            return redirect('accounts:manage_accounts')
    
    else:
        form = AccountsForm()

    template = 'accounts/accounts.html'

    context = {
        'accounts': accounts,
        'total_accounts':total_accounts,
        'total_sub_accounts':total_sub_accounts,
        'last_accounts_code':last_accounts_code,
        'form':form,
    }

    return render(request,template,context)

def edit_accounts(request,pk):
    
    
    accounts = Accounts.objects.all()
    account = accounts.get(id=pk)
    total_accounts = accounts.count()
    sub_accounts=Sub_Accounts.objects.all()
    total_sub_accounts = sub_accounts.count()
    last_accounts_code = accounts.last()
    last_sub_accounts_code = sub_accounts.last()
    
    if request.method == 'POST':
        form = AccountsForm(request.POST,instance=account)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Updated')
            return redirect('accounts:manage_accounts')
    
    else:
        form = AccountsForm(instance=account)

    template = 'accounts/accounts.html'

    context = {
        'accounts': accounts,
        'total_accounts':total_accounts,
        'total_sub_accounts':total_sub_accounts,
        'last_accounts_code':last_accounts_code,
        'last_sub_accounts_code':last_sub_accounts_code,
        'form':form,
    }

    return render(request,template,context)



