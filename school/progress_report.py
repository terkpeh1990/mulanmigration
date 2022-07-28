from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from jinja2 import filters
from .forms import *
from .models import *
from .filters import *
from django.contrib.auth.decorators import login_required


@login_required

def list_academic_terms(request):
    
    academic_year = SessionYearModel.objects.get(status='Active')
    academic_terms = SessionTerm.objects.filter(acadamic_years=academic_year.id)
    context = {
        'academic_term': academic_terms,
       
    }
    template = 'progress_report/list_terms.html'
    return render(request, template, context)



def lists_class(request,pk):
    staff = Staffs.objects.get(id=request.user.username)
    assign_classes = Staff_Class.objects.filter(staff_id = staff.id, status = 'Assigned')
    ob = []
    for a in assign_classes:
        ob.append(a.class_id.id)

    class_list = SchClass.objects.filter(id__in=ob)
    # class_list = SchClass.objects.all()
    academic_terms = SessionTerm.objects.get(id=pk)

    context = {
        'class_list': class_list,
        'academic_terms':academic_terms,
    }

    template = 'progress_report/lists_classes.html'
    return render(request, template, context)


def lists_subject(request,pk,academic_termsid):
    classess = SchClass.objects.get(id=pk)
    class_subject = SchClass_Subjects.objects.filter(class_id=classess.id)
    academic_terms = SessionTerm.objects.get(id=academic_termsid)
   
    context = {
        'classess':  classess,
        'academic_terms':academic_terms,
        'class_subject':class_subject,
    }

    template = 'progress_report/list_subjects.html'
    return render(request, template, context)


def select_class_students(request,pk,academic_termsid,class_id):
    classes = SchClass.objects.get(id=class_id)
    academic_term = SessionTerm.objects.get(id=academic_termsid)
    class_students = Students.objects.filter(course_id=class_id,stu_status='Active')
    
    class_subject = SchClass_Subjects.objects.get(id=pk)

    context = {
        'classes':classes,
        'class_students': class_students,
        'academic_term':academic_term,
        'class_subject':class_subject,
    }

    template = 'progress_report/lists_class_students.html'
    return render(request, template, context)




def add_subject_report(request,class_id,academic_termsid,student,class_subject):
    today = datetime.datetime.now()
    classes = SchClass.objects.get(id=class_id)
    academic_term = SessionTerm.objects.get(id=academic_termsid)
    student =  Students.objects.get(id=student)
    class_subjects = SchClass_Subjects.objects.get(id=class_subject)
    subject = Subjects.objects.get(id=class_subjects.subject_id.id)
    academic_year = SessionYearModel.objects.get(status='Active')
  

    if request.method == "POST":
        sub=Subject_reportForm(request.POST)
        username =request.user.username
        staff = Staffs.objects.get(id=username)
    
        
        if sub.is_valid() :
            
            top = sub.cleaned_data['topic']
            if Daily_subject_report.objects.filter(class_id=classes,session_year_id=academic_year,term_year_id=academic_term,student_id=student,subject=subject,topic=top,report_date=today).exists():
                messages.success(request, 'Remarks Already saved')
                return redirect('school:add_subject_report', classes.id, academic_term.id,student.id, class_subjects.id)
            else:
                sub_report = sub.save(commit=False)
                sub_report.class_id = classes
                sub_report.session_year_id = academic_year
                sub_report.term_year_id = academic_term
                sub_report.student_id = student
                sub_report.status = 'pending'
                sub_report.teacher_id = staff
                sub_report.subject = subject
                sub_report.save()
                
                messages.success(request, 'Remarks Saved')
                return redirect('school:upload_pic_report',sub_report.id, classes.id, academic_term.id,student.id, class_subjects.id)
    else:

        sub=Subject_reportForm()
       

    context = {
        "sub": sub,
        'classes': classes,
        'academic_term': academic_term,
        'student': student,
        'class_subjects':class_subjects,
    }

    template = 'progress_report/create_subject_report.html'
    return render(request, template, context)

def upload_pic_report(request,pk,class_id,academic_termsid,student,class_subject):
    today = datetime.datetime.now()
    classes = SchClass.objects.get(id=class_id)
    academic_term = SessionTerm.objects.get(id=academic_termsid)
    student =  Students.objects.get(id=student)
    class_subjects = SchClass_Subjects.objects.get(id=class_subject)
    subject = Subjects.objects.get(id=class_subjects.subject_id.id)
    academic_year = SessionYearModel.objects.get(status='Active')
    rep =Daily_subject_report.objects.get(id=pk)
    try:
        pictures =Daily_Subject_report_uploads.objects.filter(report_id=rep.id)
    except Daily_Subject_report_uploads.DoesNotExist:
        pass
  
    if request.method == "POST":
     
        pic = FilesForm(request.POST,request.FILES)
      
        if  pic.is_valid():
            proof = pic.save(commit=False)
            proof.report_id = rep
            proof.save()
            messages.success(request, 'Picture Uploaded Saved')
            return redirect('school:upload_pic_report',rep.id, classes.id, academic_term.id,student.id, class_subjects.id)
    else:
        pic = FilesForm()

    context = {
       
        'pic': pic,
        'classes': classes,
        'academic_term': academic_term,
        'student': student,
        'class_subjects':class_subjects,
        'rep':rep,
        'pictures':pictures
    }

    template = 'progress_report/pic_upload.html'
    return render(request, template, context)


def view_topic_report(request,pk,):
    rep =Daily_subject_report.objects.get(id=pk)
    pictures = Daily_Subject_report_uploads.objects.filter(report_id=rep.id)[:3]
    
    context = {
       
        
        'rep':rep,
        'pictures':pictures
    }

    template = 'progress_report/view_reports.html'
    return render(request, template, context)


@login_required
def approve_remarkss(request,pk):
    rep = Daily_subject_report.objects.get(id=pk)
    rep.status = "approved"
    rep.save()
    messages.success(request, "Daily remarks approved")
    return redirect('school:view_topic_report',pk=rep.id)

@login_required
def cancel_remarkss(request, pk):
    rep = Daily_subject_report.objects.get(id=pk)
    rep.status = "cancelled"
    rep.save()
    messages.success(request, "Daily remarks approved")
    return redirect('school:view_topic_report',pk=rep.id)

@login_required
def delete_daily_reports(request,pk):
    daily = Daily_subject_report.objects.get(id=pk)
    aa = daily.class_id.id
    daily.delete()
    messages.success(request, "Daily Report deleted")
    return redirect('school:class_topic_report',aa)


def view_lists_class(request):
    class_list = SchClass.objects.all()
  

    context = {
        'class_list': class_list,
       
    }

    template = 'progress_report/view_class_list.html'
    return render(request, template, context)

def class_topic_report(request,pk):
    today = datetime.datetime.now()
    rep =Daily_subject_report.objects.filter(class_id = pk )
    
    context = {
        'rep':rep, 
    }
    template = 'progress_report/view_list_class_report.html'
    return render(request, template, context)

def parent_topic_report(request):
    parent = Parents.objects.get(id=request.user.username)
    child = Students.objects.filter(parent_id=parent.id)
    ob = []
    for a in child:
        ob.append(a.id)
    rep =Daily_subject_report.objects.filter(student_id__in=ob)
    
    context = {
        'rep':rep, 
    }
    template = 'progress_report/view_list_class_report.html'
    return render(request, template, context)


def staff_list_class(request):
    staff = Staffs.objects.get(id=request.user.username)
    assign_classes = Staff_Class.objects.filter(staff_id = staff.id, status = 'Assigned')
    ob = []
    for a in assign_classes:
        ob.append(a.class_id.id)

    class_list = SchClass.objects.filter(id__in=ob)
    context = {
        'class_list': class_list,
       
    }

    template = 'progress_report/view_class_list.html'
    return render(request, template, context)


    
def staff_view_topic_report(request,pk):
    rep =Daily_subject_report.objects.get(id=pk)
    pictures = Daily_Subject_report_uploads.objects.filter(report_id=rep.id)[:3]
    
    context = {
       
        
        'rep':rep,
        'pictures':pictures
    }

    template = 'progress_report/staff_view_report.html'
    return render(request, template, context)
