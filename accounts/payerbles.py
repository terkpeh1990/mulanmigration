from django.shortcuts import render, redirect
from .forms import *
from .models import *
from school.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *

def manage_payables(request):
    payables = Account_Payables.objects.filter(amount__gt=0.00)
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))

    myFilter = PayablesFilter(request.GET, queryset=payables)
    payables = myFilter.qs
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))
    template = 'accounts/manage_payables.html'
    context={
        'payables':payables,
        'total_payables':total_payables,
        'payable_value':payable_value,
        'myFilter':myFilter,
    }
    return render(request,template,context)



@login_required
def make_payment(request, pk):# to visit again
    ob = [1103,1200]
    accounts = Sub_Accounts.objects.filter(code__code__in=ob).order_by('sub_description')
    payables = Account_Payables.objects.get(id=pk)
    his = Pv_Payment_History.objects.filter(reference=payables.reference.id)
    st = Payment_Vouchers.objects.get(id=payables.reference.id)
    if request.method == "POST":
        form = paymentform(request.POST)
        code = request.POST.get("code")
        a,_= code.split('-----')

        if form.is_valid():
            amount_paid = form.cleaned_data['amount_paid']
            payables.amount -= amount_paid
            payables.save()
            cc=Pv_Payment_History.objects.create(reference=st, amount=amount_paid)
            # General_Ledger.objects.create(transaction_date=cc.transaction_date,sub_code=st.sub_account,description=st.description,debit=cc.amount)
            subcode = Sub_Accounts.objects.get(sub_code = a)
            company = Company_group.objects.get(name="Mulan")
            General_Ledger.objects.create(transaction_date=cc.transaction_date,sub_code=subcode,description=st.description,cedit=cc.amount)
            Bank_Cash_Ledger.objects.create(transaction_date = cc.transaction_date,sub_code=st.sub_account,description=st.description,amount = (-cc.amount))
            AExpenditure.objects.create(account_code=subcode,company = st.company,pvno = st,amount=amount_paid)
            messages.success(request, "Payment Made, General Ledger Updates")
            return redirect('accounts:make_payment',payables.id)

    else:
        form = paymentform()

    context = {
        'form': form,
        'his':his,
        'order':st,
        'payables':payables,
        'accounts':accounts,
    }
    template = 'accounts/payments.html'
    return render(request, template, context)