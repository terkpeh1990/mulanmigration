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

@login_required
def add_student(request,pk):
    pp =Parents.objects.get(id=pk)
    if request.method == "POST":
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save(commit=False)
            student.stu_status = "Active"
            student.parent_id = pp
            student.save()
            # studentsmsThread(student).start()
           
            messages.success(request, "Student Added Successfully!")
            return redirect('school:add_student_education_history', student.id)
    else:
        form = AddStudentForm()


    context = {
        "form": form,

    }

    template = 'students/add_student_template.html'
    return render(request, template, context)



@login_required
def add_student_education(request,pk):
    try:
        student = Students.objects.get(id=pk)
    except Students.DoesNotExist:
        messages.success(request, "Please Register a student")
        return redirect('school:add_student')
    
    try:
        edu=EducationHistory.objects.filter(student_id=pk)
    except EducationHistory.DoesNotExist:
        pass

    if request.method == "POST":
        form = AddEducationForm(request.POST)

        if form.is_valid():
            students = form.save(commit=False)
            students.student_id = student
            students.save()

            messages.success(request, student.firstname + "'s" +
                             " " + "Educational History Added")
            return redirect('school:add_student_education_history',student.id)
    else:

        form = AddEducationForm()

    context = {
        "form": form,
        'students':student,
        'edu':edu,

    }

    template = 'students/student_education_history.html'
    return render(request, template, context)

def remove_student_education(request,pk):
   
    edu=EducationHistory.objects.get(id=pk)
    cc = edu.student_id
    edu.delete()
    messages.success(request,'Education history Removed')
    return redirect('school:add_student_education_history',cc)
    



@login_required
def add_student_emergency(request,pk):
    
    try:
        students = Students.objects.get(id=pk)
    except Students.DoesNotExist:
        messages.success(request, "Please Register a student")
        return redirect('school:add_student',pk)
    
    try:
        emm = EmmergencyContacts.objects.filter(student_id=pk)
    except EmmergencyContacts.DoesNotExist:
        pass
    if request.method == "POST":
        form = EmmercencyForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.student_id = students
            student.save()

            messages.success(request, students.firstname+ "'s"+
                             " " + "Emmercency Contact Added")
            return redirect('school:add_student_emmergency_contact' ,students.id)
    else:

        form = EmmercencyForm()

    context = {
        "form": form,
        'students': students,
        'emm':emm,

    }

    template = 'students/emmercencycontact.html'
    return render(request, template, context)

def remove_student_emmergency_contact(request,pk):
       
    edu=EmmergencyContacts.objects.get(id=pk)
    cc = edu.student_id
    edu.delete()
    messages.success(request,'Emmergency Contact Removed')
    return redirect('school:add_student_emmergency_contact',cc)

@login_required
def add_student_medical(request,pk):
    
    try:
        students = Students.objects.get(id=pk)
    except Students.DoesNotExist:
        messages.success(request, "Please Register a student")
        return redirect('school:add_student',pk)
    
    try:
        med = MedicalHistory.objects.filter(student_id=pk)
    except MedicalHistory.DoesNotExist:
        pass


    if request.method == "POST":
        form = MedicalForm(request.POST)
        doc = DoctorForm(request.POST, instance=students)

        if form.is_valid() and doc.is_valid():
            medical = form.save(commit=False)
            medical.student_id = students
            medical.save()
            doctor =doc.save()

            messages.success(request, students.firstname + "'s" +
                             " " + "Medical Condition Added")
            return redirect('school:add_student_medical', students.id)
    else:

        form = MedicalForm()
        doc = DoctorForm(instance=students)

    context = {
        "form": form,
        'doc': doc,
        'students': students,
        'med': med,
    }

    template = 'students/medical.html'
    return render(request, template, context)

def remove_student_medical(request,pk):
       
    edu=MedicalHistory.objects.get(id=pk)
    cc = edu.student_id
    edu.delete()
    messages.success(request,'Medical Record Removed')
    return redirect('school:add_student_medical',cc)

    

@login_required
def add_student_immunization(request,pk):
    try:
        students = Students.objects.get(id=pk)
    except Students.DoesNotExist:
        messages.success(request, "Please Register a student")
        return redirect('school:add_student',pk)
    
    try:
        immu = ImmunisationHistory.objects.filter(student_id=pk)
    except ImmunisationHistory.DoesNotExist:
        pass

    if request.method == "POST":
        form = ImmunizationForm(request.POST)

        if form.is_valid():
            immune = form.save(commit=False)
            immune.student_id = students
            immune.save()

            messages.success(request, students.firstname + "'s" +
                             " " + "Immunization Added")
            return redirect('school:add_student_immunization', students.id)
    else:

        form = ImmunizationForm()

    context = {
        "form": form,
        'students': students,
        'immu':immu,

    }

    template = 'students/immunization.html'
    return render(request, template, context)

def remove_student_immunization(request,pk):
       
    edu=ImmunisationHistory.objects.get(id=pk)
    cc = edu.student_id
    edu.delete()
    messages.success(request,'Immunization Record Removed')
    return redirect('school:add_student_immunization',cc)



@login_required
def delete_student(request, pk):
    stu = Students.objects.get(id=pk)
    try:
        stu.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('school:manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('school:manage_student')

@login_required
def student_profile(request,pk):
    try:
        students= Students.objects.get(id=pk)
    except Students.DoesNotExist:
        pass

    try:
        student_education = EducationHistory.objects.filter(student_id=pk)
    except EducationHistory.DoesNotExist:
        pass

    try:
        student_emmergency_contact = EmmergencyContacts.objects.filter(student_id=pk)
    except EmmergencyContacts.DoesNotExist:
        pass
    try:
        student_medical_history = MedicalHistory.objects.filter(student_id=pk)
    except MedicalHistory.DoesNotExist:
        pass

    try:
        student_immunization_history = ImmunisationHistory.objects.filter(student_id=pk)
    except ImmunisationHistory.DoesNotExist:
        pass

    template = 'students/student_profile.html'

    context = {
        'students':students,
        'student_education': student_education,
        'student_emmergency_contact': student_emmergency_contact,
        'student_medical_history': student_medical_history,
        'student_immunization_history':student_immunization_history,
    }

    return render(request, template, context)


@login_required
def edit_student_education(request, pk):
    stuedu = EducationHistory.objects.get(id=pk)
    studid = stuedu.student_id_id

    students = Students.objects.get(id=studid)

    if request.method == "POST":
        form = AddEducationForm(request.POST, instance=stuedu)

        if form.is_valid():
            parent = form.save()
            messages.success(request, "Educational History Updated!")
            return redirect('school:student_profile', pk=students.id)
    else:
        form = AddEducationForm(instance=stuedu)
    context = {
        "form": form,
        'students': students,
    }
    template = 'students/student_education_history.html'
    return render(request, template, context)

@login_required
def edit_student_emmergency(request, pk):
    stuedu = EmmergencyContacts.objects.get(id=pk)
    studid = stuedu.student_id_id

    students = Students.objects.get(id=studid)

    if request.method == "POST":
        form = EmmercencyForm(request.POST, instance=stuedu)

        if form.is_valid():
            parent = form.save()
            messages.success(request, "Emmergency  Contact Updated!")
            return redirect('school:student_profile', pk=students.id)
    else:
        form = EmmercencyForm(instance=stuedu)
    context = {
        "form": form,
        'students': students,
    }
    template = 'students/emmercencycontact.html'
    return render(request, template, context)


@login_required
def edit_student_medical(request, pk):
    stuedu = MedicalHistory.objects.get(id=pk)
    studid = stuedu.student_id_id

    students = Students.objects.get(id=studid)

    if request.method == "POST":
        form = MedicalForm(request.POST, instance=stuedu)

        if form.is_valid():
            parent = form.save()
            messages.success(request, "Medical History Updated!")
            return redirect('school:student_profile', pk=students.id)
    else:
        form = MedicalForm(instance=stuedu)
    context = {
        "form": form,
        'students': students,
    }
    template = 'students/medicaledit.html'
    return render(request, template, context)


@login_required
def edit_student_immunization(request, pk):
    stuedu = ImmunisationHistory.objects.get(id=pk)
    studid = stuedu.student_id_id

    students = Students.objects.get(id=studid)

    if request.method == "POST":
        form = ImmunizationForm(request.POST, instance=stuedu)

        if form.is_valid():
            parent = form.save()
            messages.success(request, "Immunization History Updated!")
            return redirect('school:student_profile', pk=students.id)
    else:
        form = ImmunizationForm(instance=stuedu)
    context = {
        "form": form,
        'students': students,
    }
    template = 'students/immunization.html'
    return render(request, template, context)

@login_required
def delete_student_education(request, pk):
    par = EducationHistory.objects.get(id=pk)
    studid = par.student_id_id

    students = Students.objects.get(id=studid)
    try:
        stu = students.id
        par.delete()
        messages.success(request, "Educational History Deleted")
        return redirect('school:student_profile', pk=stu)
    except:
        messages.error(request, "Failed to Delete Educational History.")
        return redirect('school:student_profile', pk=stu)


@login_required
def delete_student_emmergency(request, pk):
    par = EmmergencyContacts.objects.get(id=pk)
    studid = par.student_id_id

    students = Students.objects.get(id=studid)
    try:
        stu = students.id
        par.delete()
        messages.success(request, "Emmergency Contact Deleted")
        return redirect('school:student_profile', pk=stu)
    except:
        messages.error(request, "Failed to Delete Emmergency Contact.")
        return redirect('school:student_profile', pk=stu)


@login_required
def delete_student_medical(request, pk):
    par = MedicalHistory.objects.get(id=pk)
    studid = par.student_id_id

    students = Students.objects.get(id=studid)
    try:
        stu = students.id
        par.delete()
        messages.success(request, "Medical History Deleted")
        return redirect('school:student_profile', pk=stu)
    except:
        messages.error(request, "Failed to Delete Medical History.")
        return redirect('school:student_profile', pk=stu)


@login_required
def delete_student_immunization(request, pk):
    par = ImmunisationHistory.objects.get(id=pk)
    studid = par.student_id_id

    students = Students.objects.get(id=studid)
    try:
        stu = students.id
        par.delete()
        messages.success(request, "Immunization History Deleted")
        return redirect('school:student_profile', pk=stu)
    except:
        messages.error(request, "Failed to Delete Immunization History.")
        return redirect('school:student_profile', pk=stu)


@login_required
def add_profile_student_education(request, pk):

    students = Students.objects.get(id=pk)

    if request.method == "POST":
        form = AddEducationForm(request.POST)

        if form.is_valid():
            st = form.save(commit=False)
            st.student_id = students
            st.save()
            messages.success(request, "Educational History Added!")
            return redirect('school:student_profile', pk=students.id)
    else:
        form = AddEducationForm()
    context = {
        "form": form,
        'students': students,
    }
    template = 'students/student_education_history.html'
    return render(request, template, context)


@login_required
def add_profile_student_emmergency(request, pk):

    students = Students.objects.get(id=pk)

    if request.method == "POST":
        form = EmmercencyForm(request.POST)

        if form.is_valid():
            st = form.save(commit=False)
            st.student_id = students
            st.save()
            messages.success(request, "Emmergency Contact Added!")
            return redirect('school:student_profile', pk=students.id)
    else:
        form = EmmercencyForm()
    context = {
        "form": form,
        'students': students,
    }
    template = 'students/emmercencycontact.html'
    return render(request, template, context)

@login_required
def add_profile_student_medical(request, pk):

    students = Students.objects.get(id=pk)

    if request.method == "POST":
        form = MedicalForm(request.POST)

        if form.is_valid():
            st = form.save(commit=False)
            st.student_id = students
            st.save()
            messages.success(request, "Medical History Added!")
            return redirect('school:student_profile', pk=students.id)
    else:
        form = MedicalForm()
    context = {
        "form": form,
        'students': students,
    }
    template = 'students/medicaledit.html'
    return render(request, template, context)


@login_required
def add_profile_student_immunization(request, pk):

    students = Students.objects.get(id=pk)

    if request.method == "POST":
        form = ImmunizationForm(request.POST)

        if form.is_valid():
            st = form.save(commit=False)
            st.student_id = students
            st.save()
            messages.success(request, "Immunization History Added!")
            return redirect('school:student_profile', pk=students.id)
    else:
        form = ImmunizationForm()
    context = {
        "form": form,
        'students': students,
    }
    template = 'students/immunization.html'
    return render(request, template, context)


@login_required
def edit_student(request,pk):
    stud = Students.objects.get(id=pk)
    if request.method == "POST":
        form = EditStudentForm(request.POST, request.FILES, instance=stud)

        if form.is_valid():
            student = form.save()
            messages.success(request, "Student Record Updated")
            return redirect('school:student_profile', pk=pk)
    else:
        form = EditStudentForm(instance=stud)

    context = {
        "form": form,

    }

    template = 'students/editstudent.html'
    return render(request, template, context)

@login_required
def manage_student(request):
    student_list = Students.objects.all().order_by('-id')

    context = {
        'student_list': student_list,
    }

    template = 'students/manage_student.html'
    return render(request, template, context)



@login_required
def activate_status(request, pk):
    stu = Students.objects.get(id=pk)
    stu.stu_status = 'Active'   
    stu.save()
    messages.success(request, "Student Activated")
    return redirect('school:student_profile',stu.id)
    

def deactivate_status(request, pk):
    stu = Students.objects.get(id=pk)
    stu.stu_status = 'Inactive'
    stu.save()
    messages.error(request, "Student Deactivated")
    return redirect('school:student_profile',stu.id)