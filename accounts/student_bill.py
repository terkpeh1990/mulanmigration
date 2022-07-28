from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *

from school.models import SessionTerm,SessionYearModel,Students,Parents



def students(request):
    students = Students.objects.exclude(stu_status = 'Inactive')

    context = {
        'students': students,
    }

    template = 'accounts/list_students.html'
    return render(request, template, context)


def list_active_academic_terms(request,pk):
    student = Students.objects.get(id=pk)
    academic_year = SessionYearModel.objects.get(status='Active')
    academic_terms = SessionTerm.objects.filter(acadamic_years=academic_year.id)
    context = {
        'academic_term': academic_terms,
        'student':student,
    }
    template = 'accounts/list_terms.html'
    return render(request, template, context)


def create_bill(request,academicterm_id,student_id):
    student = Students.objects.get(id=student_id)
    academic_year = SessionYearModel.objects.get(status='Active')
    academic_term = SessionTerm.objects.get(id=academicterm_id)
    bill = Student_Bill.objects.create(student_id=student,session_year_id=academic_year,term_year_id=academic_term,parent_id=student.parent_id.id,bill_status=True)
    return redirect('accounts:student_bill_details',bill.id)

def student_bill_details(request,pk):
    bill = Student_Bill.objects.get(id=pk)
    try:
        detail = Student_Bill_Details.objects.filter(bill_id=bill.id)
    except Student_Bill_Details.DoesNotExist:
        pass
    try:
        arreas = Account_Receivable.objects.filter(student_id=bill.student_id.id)
        for i in arreas:
            print(i.amount)

    except Account_Receivable.DoesNotExist:
        pass
    form = Student_Bill_Detail_Form()

    if detail:
        gross_total = detail.aggregate(cc=Sum('amount'))
        bill.amount = gross_total['cc']
        bill.balance = gross_total['cc']
        bill.save()
    else:
        gross_total = 0.00
        bill.amount = gross_total
        bill.save()

    if arreas:
        arreas_total = arreas.aggregate(bb=Sum('amount'))
        total = float(bill.amount) + float(arreas_total['bb'])
    else:
        arreas_total = 0.00
        total = bill.amount


    if request.method =='POST':
        form = Student_Bill_Detail_Form(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.bill_id = bill
            form.save()
            messages.success(request, 'Bill item added')
            return redirect('accounts:student_bill_details',bill.id)

    template = 'accounts/bill_details.html'
    context ={
        'bill':bill,
        'detail':detail,
        'gross_total':gross_total,
        'form':form,
        'total':total,
        'arreas_total':arreas_total,

    }
    return render(request, template, context)


def deletes_billitems(request,pk):
    pro = Student_Bill_Details.objects.get(id=pk)
    pv = Student_Bill.objects.get(id=pro.bill_id.id)
    pro.delete()

    return redirect('accounts:student_bill_details',pv.id)



def manage_bills(request):
    bills = Student_Bill.objects.filter(amount__gt=0.00)
    total = bills.aggregate(cc=Sum('amount'))
    bill_count = bills.count()

    context = {
        'bills': bills,
        'total': total,
        'bill_count':bill_count,
    }
    template = 'accounts/manage_student_bill.html'
    return render(request, template, context)


def apply_discount(request,pk):
    bills = Student_Bill.objects.get(id=pk)
    today =datetime.date.today()

    if request.method == 'POST':
        form = Discountform(request.POST)
        if form.is_valid():
            discount_percentage = form.cleaned_data['discount']
            receivable = Account_Receivable.objects.get(student_id= bills.student_id.id)
            percentage_decimal = discount_percentage/100
            value = bills.amount * percentage_decimal
            if receivable.amount == 0.00:
                messages.success(request, 'Discount cannot be applied on a 0 receivables')
                return redirect('accounts:apply_discount' , bills.id)
            elif receivable.amount < value:
                messages.success(request, 'Discount cannot be applied a discount geater than students receivables')
                return redirect('accounts:apply_discount' , bills.id)
            else:
                bills.amount -= value
                bills.balance -= value
                bills.discount = value
                bills.save()

                Discounts.objects.create(discount_value=value)
                receivable = Account_Receivable.objects.get(student_id= bills.student_id.id)
                receivable.amount -= value
                receivable.save()
                code= Sub_Accounts.objects.get(sub_code = 3002)
                General_Ledger.objects.create(transaction_date=today,sub_code=code,description=bills.student_id.id +'--'+bills.student_id.Surname+ " "+bills.student_id.firstname +" "+"bill adjusted with discount",debit=value)
                messages.success(request, str(discount_percentage) + '%' + ' '+ 'applied')
                return redirect('accounts:apply_discount' , bills.id)
    else:
        form = Discountform()

    context = {
        'bills': bills,
        'form':form,
    }
    template = 'accounts/discount.html'
    return render(request, template, context)




def view_student_bill(request,pk):
    bill = Student_Bill.objects.get(id=pk)
    try:
        detail = Student_Bill_Details.objects.filter(bill_id=bill.id)
    except Student_Bill_Details.DoesNotExist:
        pass
    try:
        arreas = Account_Receivable.objects.filter(student_id=bill.student_id.id)


    except Account_Receivable.DoesNotExist:
        pass





    total = bill.amount




    template = 'accounts/view_bill.html'
    context ={
        'bill':bill,
        'detail':detail,

        'total':total,


    }
    return render(request, template, context)



def run_student_bills(request):
    today =datetime.date.today()
    bills = Student_Bill.objects.filter(bill_status=True,amount__gt=0.00)
    code= Sub_Accounts.objects.get(sub_code = 3002)
    for a in bills:
        if Account_Receivable.objects.filter(student_id=a.student_id).exists():
            arreas = Account_Receivable.objects.get(student_id=a.student_id.id)
            arreas.amount += a.amount
            arreas.save()
            a.bill_status = False
            a.save()
            pass

        else:
            Account_Receivable.objects.create(transaction_date=today,sub_code=code,description=a.student_id.id +'--'+a.student_id.Surname+ " "+a.student_id.firstname +" "+"bill",amount=a.amount,student_id=a.student_id)
            a.bill_status = False
            a.save()
        General_Ledger.objects.create(transaction_date=today,sub_code=code,description=a.student_id.id +'--'+a.student_id.Surname+ " "+a.student_id.firstname +" "+"bill",cedit=a.amount)
    messages.success(request,'Accounts Updated')
    return redirect('accounts:manage_bills')

def parent_see_bill(request):
    parent = Parents.objects.get(id=request.user.username)
    child = Students.objects.filter(parent_id=parent.id)
    bills = Student_Bill.objects.filter(student_id__parent_id=parent.id)


    context = {
        'bills': bills,

    }
    template = 'accounts/parent_bills.html'
    return render(request, template, context)
