from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *
from bakery.models import BClosing_Stock_summery
from partytree.models import Closing_Stock_summery



def account_dashboards(request):
    receivables = Account_Receivable.objects.all()
    payables = Account_Payables.objects.all()
    bank = fees_transaction.objects.all()

    ob = [1103,1200]
    cash = Sub_Accounts.objects.filter(code__code__in=ob).exclude(sub_code=1201)

    bakesclosing_stock = BClosing_Stock_summery.objects.last()
    partytreeclosing_stock =  Closing_Stock_summery.objects.last()




    receivables_value = receivables.aggregate(cc=Sum('amount'))
    payables_value = payables.aggregate(cc=Sum('amount'))
    cash_value =cash.values('sub_code').annotate(c =Sum('bank_cash_ledger__amount'),).values('sub_description','c').exclude(c__lte=0).order_by('c')
    template = 'accounts/accdashboard.html'
    context={

        'receivables_value':receivables_value,
        'payables_value':payables_value,
        'bakesclosing_stock':bakesclosing_stock,
        'partytreeclosing_stock':partytreeclosing_stock,
        'bank':bank,
        'cash_value':cash_value,


    }
    return render(request,template,context)