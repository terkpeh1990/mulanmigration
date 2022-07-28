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
import datetime


def list_active_academic_terms(request):
    academic_year = SessionYearModel.objects.get(status='Active')
    academic_terms = SessionTerm.objects.filter(acadamic_years=academic_year.id)
    context = {
        'academic_term': academic_terms,
    }

    template = 'attendance/list_academicterms.html'
    return render(request, template, context)

def select_attendance_class(request,pk):
    academic_terms = SessionTerm.objects.get(id=pk)
    if request.user.profile.is_staff:
        staff = Staffs.objects.get(id=request.user.username)
        assign_classes = Staff_Class.objects.filter(staff_id = staff.id, status = 'Assigned')
        ob = []
        for a in assign_classes:
            ob.append(a.class_id.id)

        school_classes = SchClass.objects.filter(id__in=ob)
        # school_classes = Staff_Class.objects.filter(staff_id=request.user.username,acadamic_year=academic_terms.acadamic_years)
    else:
        school_classes = SchClass.objects.all()

    context = {
        'school_classes': school_classes,
        'academic_term': academic_terms,
    }
    template = 'attendance/list_attendance_classes.html'
    return render(request, template, context)


def create_attendance(request,pk,accadermic_terms_id):
    academic_terms = SessionTerm.objects.get(id=accadermic_terms_id)
    academic_year = SessionYearModel.objects.get(id=academic_terms.acadamic_years.id)
    school_class = SchClass.objects.get(id=pk)
    today = datetime.datetime.now()
    try:
        Attendance.objects.get(class_id=school_class,session_year_id=academic_year ,term_year_id=academic_terms,attendance_date=today)
        messages.success(request,'Today Class Attendence for'+ ' '+ school_class.class_name + ' ' +'Already Exist')
        return redirect('school:select_attendance_class',pk=academic_terms.id)
    except Attendance.DoesNotExist:
        daily_attendance=Attendance.objects.create(class_id=school_class,session_year_id=academic_year ,term_year_id=academic_terms)
        return redirect('school:take_attendance', pk =daily_attendance.id)


@login_required
def manage_attendance(request):
    today = datetime.datetime.now()
    attendance_list = Attendance.objects.filter(attendance_date__month= today.month
        ).order_by('-id')
    context = {
        'academic_term': attendance_list,
    }

    template = 'attendance/manage_attendance.html'
    return render(request, template, context)


@login_required
def delete_attendance(request, pk):
    acad = Attendance.objects.get(id=pk)
    try:
        acad.delete()
        messages.success(request, "Attendance deleted")
        return redirect('school:manage_attendance')
    except:
        messages.error(request, "Failed to Attendance.")
        return redirect('school:manage_attendance')





@login_required
def take_attendance(request, pk):

    attendance = Attendance.objects.get(id=pk)
    stu = Students.objects.filter(stu_status='Active',course_id=attendance.class_id)
    for a in stu:
        print(a.id)

    context = {
        'stu': stu,
        'attendance':attendance,

    }
    template = 'attendance/take_attendance.html'
    return render(request, template, context)

@login_required
def finish_attendance(request,pk):

    attendance = Attendance.objects.get(id=pk)
    stu = Students.objects.filter(course_id=attendance.class_id)
    for s in stu:
        s.att = False
        s.save()
    return redirect('school:manage_attendance')

@login_required
def present(request,pk,attendance_id):
    stu = Students.objects.get(id=pk)

    att = Attendance.objects.get(id = attendance_id)
    if AttendanceReport.objects.filter(student_id=stu, attendance_id=att).exists():
        messages.success(request,'Student attendance taken already')
        return redirect('school:take_attendance', pk=attendance_id)
        pass
    else:
        AttendanceReport.objects.create(student_id=stu, attendance_id=att, status=True)
    # stu.att = True
    # stu.save()
    return redirect('school:take_attendance', pk=attendance_id)


@login_required
def absent(request, pk,attendance_id):
    stu = Students.objects.get(id=pk)
    att = Attendance.objects.get(id = attendance_id)
    if AttendanceReport.objects.filter(student_id=stu, attendance_id=att).exists():
        messages.success(request,'Student attendance taken already')
        return redirect('school:take_attendance', pk=attendance_id)
        pass
    else:
        AttendanceReport.objects.create(student_id=stu, attendance_id=att, status=False)

    stu.att = True
    stu.save()
    return redirect('school:take_attendance', pk=attendance_id)



@login_required
def view_attendance(request,pk):

    stu = AttendanceReport.objects.filter(attendance_id=pk)
    ff = Attendance.objects.get(id=pk)

    context = {
        'stu': stu,
        'ff':ff,
    }
    template = 'attendance/view_attendance.html'
    return render(request, template, context)


@login_required
def epresent(request, pk):
    stu = AttendanceReport.objects.get(id=pk )
    stu.status = True
    stu.save()
    return redirect('school:view_attendance', pk=stu.attendance_id)


@login_required
def eabsent(request, pk):
    stu = AttendanceReport.objects.get(id=pk)
    stu.status = False
    stu.save()
    return redirect('school:view_attendance', pk=stu.attendance_id)


@login_required
def attendance_report(request):

    att = AttendanceReport.objects.all()
    total = att.count()
    present = att.filter(status=True).count()
    absent= att.filter(status=False).count()
    myFilter = AttendanceFilter(request.GET, queryset=att)
    att =myFilter.qs
    total = att.count()
    present = att.filter(status=True).count()
    absent= att.filter(status=False).count()

    context = {
        'att': att,
        'total':total,
        'present':present,
        'absent':absent,
        'myFilter':myFilter,
    }
    template = 'attendance/attendance_report.html'
    return render(request, template, context)

@login_required
def staff_manage_attendance(request):
    staff = Staffs.objects.get(id=request.user.username)
    assign_classes = Staff_Class.objects.filter(staff_id = staff.id, status = 'Assigned')
    ob = []
    for a in assign_classes:
        ob.append(a.class_id.id)

    # class_list = SchClass.objects.filter(id__in=ob)
    today = datetime.datetime.now()
    attendance_list = Attendance.objects.filter(attendance_date__month= today.month,class_id__in = ob
        )
    context = {
        'academic_term': attendance_list,
    }

    template = 'attendance/manage_attendance.html'
    return render(request, template, context)



def staff_attendance_report(request):

    att = AttendanceReport.objects.all()
    total = att.count()
    present = att.filter(status=True).count()
    absent= att.filter(status=False).count()
    myFilter = StaffAttendanceFilter(request.GET, queryset=att)
    att =myFilter.qs
    total = att.count()
    present = att.filter(status=True).count()
    absent= att.filter(status=False).count()

    context = {
        'att': att,
        'total':total,
        'present':present,
        'absent':absent,
        'myFilter':myFilter,
    }
    template = 'attendance/teachers.html'
    return render(request, template, context)