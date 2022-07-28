from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import *

def general_ledger(request):
   
    try:
        general_ledger= General_Ledger.objects.all()
    except General_Ledger.DoesNotExist:
        pass
         
    accounts = Sub_Accounts.objects.all()  

    myFilter = GeneralLedgerFilter(request.GET, queryset=general_ledger)
    general_ledger = myFilter.qs
    

    if request.method =='POST':
        form=General_LedgerForm(request.POST)
        debits = request.POST.get("debitcode")
        credits = request.POST.get("creditcode")
        a,_= debits.split('-----')
        b,_= credits.split('-----')
        
        
        
        if form.is_valid():
            transaction_date = form.cleaned_data.get('transaction_date')
            debt_amount = form.cleaned_data.get('debt_amount')
            description = form.cleaned_data.get('description')
            credit_amount = form.cleaned_data.get('credit_amount')
           
    
            debt_sub_acount = Sub_Accounts.objects.get(sub_code=a)
            credit_sub_acount = Sub_Accounts.objects.get(sub_code=b) 
            debit_transaction=General_Ledger.objects.create(transaction_date=transaction_date,sub_code=debt_sub_acount,description=description,debit=debt_amount)
            # subcode = Sub_Accounts.objects.get(id =debit_transaction.sub_code.id)
            # account = Accounts.objects.get(id = subcode.code.id)
            # print(account.code)
            # if account.code == 1103 or account.code == 1200:
            #     Bank_Cash_Ledger.objects.create(transaction_date=transaction_date,sub_code=debt_sub_acount,description=description,amount=debt_amount)
          
            # credit_transaction=General_Ledger.objects.create(transaction_date=transaction_date,sub_code=credit_sub_acount,description=description,cedit=credit_amount)
            # csubcode = Sub_Accounts.objects.get(id =credit_transaction.sub_code.id)
            # caccount = Accounts.objects.get(id = csubcode.code.id)
            # print(caccount.code)
            # if caccount.code == 1103 or caccount.code == 1200:
            #     Bank_Cash_Ledger.objects.create(transaction_date=transaction_date,sub_code=debt_sub_acount,description=description,amount=(-credit_amount))
           
            messages.success(request,"General Ledger recorded")
            return redirect('accounts:general_ledger')
    else:
        form = General_LedgerForm()
    
    template = 'accounts/general_ledger.html'
    context ={
            "accounts": accounts,
            "general_ledger": general_ledger,
            'form':form,
            'myFilter':myFilter,
            
        }
    return render(request, template, context)
