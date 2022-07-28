from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from accounts import receivables
from .forms import *
from .models import *
from .filters import *
from .utils import *
import datetime
from accounts.models import Account_Receivable,fees_transaction


@login_required
def parentdashboard(request):
    parent = Parents.objects.get(id=request.user.username)
    child = Students.objects.filter(parent_id=parent.id)
    receivables = Account_Receivable.objects.filter(student_id__parent_id=parent.id)
    children = child.count()
    current_bill =  receivables.aggregate(cc=Sum('amount'))
    # for a in child:
    #     print (a.id)
    ob = []
    for a in child:
        ob.append(a.id)

    fees = fees_transaction.objects.filter(student_id__in=ob)
    
   
 

    context={
        'parent':parent,
        'ord': ord,
        'children': children,
      
        'child': child,
        'receivables':receivables,
        'current_bill':current_bill,
        'fees':fees
    }

    template ='hod_template/parentdashboard.html'
    return render(request,template,context)


@login_required
def parentbill(request,pk):
    # studbill = StudentBill.objects.get(id=pk)
    stud = Students.objects.get(id=pk)
    # bb = Bills.objects.get(id=stud.course)
    bill = Bills.objects.filter(
        class_id=stud.course_id)

    context = {
        'bill': bill,
        # 'arres': arres,
        # 'studbill': studbill,
    }

    template='hod_template/manage_bill.html'
    return render(request,template)


@login_required
def child_results(request):
    attendance_list = studenthistory.objects.filter(
        parent_id=request.user.username).order_by('-results')
    context = {
        'academic_term': attendance_list,
    }

    template = 'staff_template/manage_resultss.html'
    return render(request, template, context)


def parentdailyreport(request):
    rep = DailyClassReportDetails.objects.filter(status='approved',
        parent_id=request.user.username).order_by('-id')
    template = 'hod_template/view_dailyreport.html'
    context = {
        'rep': rep,
    }
    return render(request, template, context)
