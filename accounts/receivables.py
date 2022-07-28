from django.shortcuts import render, redirect
from .forms import *
from .models import *
from school.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *
import datetime

def manage_receivables(request):
    payables = Account_Receivable.objects.filter(amount__gt=0.00)
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))

    myFilter = ReceivableFilter(request.GET, queryset=payables)
    payables = myFilter.qs
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))
    template = 'accounts/receivables.html'
    context={
        'payables':payables,
        'total_payables':total_payables,
        'payable_value':payable_value,
        'myFilter':myFilter,
    }
    return render(request,template,context)

@login_required
def receive_payment(request, pk):# to visit again
    ob = [1103,1200]
    today =datetime.date.today()
    accounts = Sub_Accounts.objects.filter(code__code__in=ob).order_by('sub_description')

    payables = Account_Receivable.objects.get(id=pk)
    student  = Students.objects.get(id=payables.student_id.id)
    his = fees_transaction.objects.filter(student_id=student.id)
    if request.method == "POST":
        form = paymentform(request.POST)
        code = request.POST.get("code")
        a,_= code.split('-----')

        if form.is_valid():
            amount_paid = form.cleaned_data['amount_paid']
            payables.amount -= amount_paid
            payables.save()
            aa = amount_paid
            bb=fees_transaction.objects.create(amount=amount_paid,balance=payables.amount,student_id=student.id)
            company = Company_group.objects.get(name="Mulan")
            # General_Ledger.objects.create(transaction_date=cc.transaction_date,sub_code=st.sub_account,description=st.description,debit=cc.amount)
            subcode = Sub_Accounts.objects.get(sub_code = a)
            General_Ledger.objects.create(transaction_date=today,sub_code=subcode,description="Payment of Fees. Paid on Premise",debit=amount_paid)
            Bank_Cash_Ledger.objects.create(transaction_date=today,sub_code=subcode,description='Payment of Fees. Paid on Premise',amount = amount_paid)
            ARevenue.objects.create(account_code=subcode,status="Cash",company = company,amount=amount_paid,close='Old')
            # BankThread(bb)
            messages.success(request, "Payment Made, General Ledger Updates")
            return redirect('accounts:student_account',payables.id)

    else:
        form = paymentform()

    context = {
        'form': form,
        'payables':payables,
        'accounts':accounts,
        'his':his,
    }
    template = 'accounts/rec_payment.html'
    return render(request, template, context)



def sales(request):

    ord = ARevenue.objects.all()
    total = ord.aggregate(cc=Sum('amount'))
    od = ord.count()
    myFilter = ARevenueFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = ord.aggregate(cc=Sum('amount'))
    od = ord.count()
    template = 'accounts/sales.html'
    context = {
        'ord': ord,
        'total': total,
        'od': od,
        'myFilter':myFilter,
    }
    return render(request, template, context)


def student_account(request,pk):
    payables = Account_Receivable.objects.get(id=pk)
    student  = Students.objects.get(id=payables.student_id.id)
    his = fees_transaction.objects.filter(student_id=student.id)
    bills = Student_Bill.objects.filter(student_id=student.id)

    context = {

        'bills':bills,
        'payables':payables,
        'his':his,
    }
    template = 'accounts/student_account.html'
    return render(request, template, context)


def view_individual_bill(request,pk,rec):
    payables = Account_Receivable.objects.get(id=rec)
    bill = Student_Bill.objects.get(id=pk)
    try:
        detail = Student_Bill_Details.objects.filter(bill_id=bill.id)
    except Student_Bill_Details.DoesNotExist:
        pass
    total = bill.amount


    template = 'accounts/view_individual_bill.html'
    context ={
        'bill':bill,
        'detail':detail,

        'total':total,
        'payables':payables,

    }
    return render(request, template, context)
