from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .forms import *
from .models import *
from bakery.models import *
from partytree.models import *
from salon.models import *
from .filters import *
from twilio.rest import TwilioRestClient
from twilio.rest import Client
from school_management_system.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from django.utils.html import strip_tags
from accounts.models import Payment_Vouchers,fees_transaction,Account_Receivable,Account_Payables,Sub_Accounts

def principaldashboard(request):
    all_student_count = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    student_list = Students.objects.all()
    active_students = Students.objects.filter(stu_status="Active").count()
    Inactive_students = Students.objects.filter(stu_status="Inactive").count()
    staff_count = Staffs.objects.all().count()

    ob = [1103,1200]

    cash = Sub_Accounts.objects.filter(code__code__in=ob).exclude(sub_code=1201)

    receivables = Account_Receivable.objects.all()
    payables = Account_Payables.objects.all()

    bank = fees_transaction.objects.all()
    receivables_value = receivables.aggregate(cc=Sum('amount'))
    payables_value = payables.aggregate(cc=Sum('amount'))
    cash_value =cash.values('sub_code').annotate(c =Sum('bank_cash_ledger__amount'),).values('sub_description','c').exclude(c__lte=0).order_by('c')

    bakesclosing_stock = BClosing_Stock_summery.objects.last()
    partytreeclosing_stock =  Closing_Stock_summery.objects.last()

    obs =['Pending','pending']

    pending_pvs = Payment_Vouchers.objects.filter(status__in = obs)





    context ={

        'all_student_count': all_student_count,
        'student_list': student_list,
        'active_students': active_students,
        'Inactive_students':Inactive_students,
        'bank':bank,
        'receivables_value':receivables_value,
        'payables_value':payables_value,
        'cash_value':cash_value,
        'bakesclosing_stock':bakesclosing_stock,
        'partytreeclosing_stock':partytreeclosing_stock,


        'staff_count': staff_count,

        'pending_pvs': pending_pvs,




    }

    template='hod_template/principal.html'
    return render(request,template,context)

