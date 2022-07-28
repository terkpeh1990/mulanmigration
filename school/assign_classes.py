from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .forms import *
from .models import *
from .filters import *
from twilio.rest import TwilioRestClient
from twilio.rest import Client
from school_management_system.settings import  TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
# proxy_client
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .parentthread import *

def assign_student_class(request,pk):
    student = Students.objects.get(id=pk)
    if request.method == "POST":
        form = AssignClassForm(request.POST)

        if form.is_valid():
            today = datetime.date.today()
            acadyear = SessionYearModel.objects.get(status='Active')
            stud_class = form.cleaned_data['class_id']
            stud_cla = SchClass.objects.get(class_name=stud_class)
            
            bb=Students_Class.objects.filter(class_id=stud_cla,student_id=student,acadamic_years=acadyear)
            
            if bb.exists():
                messages.success(
                request, "Student Already Exist In This Class For This Academic Year")
                return redirect('school:assign_student_class' ,student.id)
            else:
                aa=Students_Class.objects.create(class_id=stud_cla,student_id=student,acadamic_years=acadyear)
                student.course_id=aa.class_id
                student.save()
                messages.success(
                request, "Class Assigned Successfully")
                return redirect('school:assign_student_class' ,student.id)

           
    else:
        form = AssignClassForm()

    context = {
        "form": form,
        'students':student,
    }
    template = 'class_assignment/assign_student_class.html'
    return render(request, template, context)

def run_class(request):
    students = Students.objects.all()
    acadyear = SessionYearModel.objects.get(status='Active')
    for student in students:
        if student.course_id:
            try:
                Students_Class.objects.filter(class_id=student.course_id,student_id=student,acadamic_years=acadyear)

            except Students_Class.DoesNotExist:
                Students_Class.objects.create(class_id=student.course_id,student_id=student,acadamic_years=acadyear)
        else:
            pass
    messages.success(request,"Classes Assigned")
    return redirect('school:manage_student')


def assign_staff_class(request,pk):
    student = Staffs.objects.get(id=pk)
    ass_classes = Staff_Class.objects.filter(staff_id=student.id).order_by('-id')
    if request.method == "POST":
        form = AssignClassForm(request.POST)

        if form.is_valid():
            today = datetime.date.today()
            acadyear = SessionYearModel.objects.get(status='Active')
            stud_class = form.cleaned_data['class_id']
            stud_cla = SchClass.objects.get(class_name=stud_class)

            Staff_Class.objects.create(class_id=stud_cla,staff_id=student,acadamic_year=acadyear)
            messages.success(
                    request, "Class Assigned Successfully")
            return redirect('school:assign_staff_class' ,student.id)
    else:
        form = AssignClassForm()

    context = {
        "form": form,
        'students':student,
        'ass_classes':ass_classes,
    }
    template = 'class_assignment/assign_staff_class.html'
    return render(request, template, context)

def run_stfclass(request):
    students = Students.objects.all()
    acadyear = SessionYearModel.objects.get(status='Active')
    for student in students:
        
        student.att = False
        student.save()
        
    messages.success(request,"Classes Assigned")
    return redirect('school:manage_staff')


def unassign_class(request,pk):
    ass_classes = Staff_Class.objects.get(id=pk)
    ass_classes.status = 'Unassigned'
    ass_classes.save()
    messages.success(request,"Classes Unassigned")
    return redirect('school:assign_staff_class' , ass_classes.staff_id.id)