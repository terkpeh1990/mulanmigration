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
from accounts.models import ARevenue


@login_required
def add_parent(request):
    if request.method == "POST":
        form = AddParentForm(request.POST)
        if form.is_valid():
            parent = form.save()
            # ParentsmsThread(parent).start()
            messages.success(request, "Parent Added Successfully!")
            return redirect('school:manage_parent')
    else:
        form = AddParentForm()
    context = {
        "form": form,
    }
    template = 'hod_template/add_parent.html'
    return render(request, template, context)

@login_required
def edit_parent(request, pk):
    par = Parents.objects.get(id = pk)
    if request.method == "POST":
        form = AddParentForm(request.POST, instance=par)

        if form.is_valid():
            parent = form.save()
            messages.success(request, "Parent Added Successfully!")
            return redirect('school:manage_parent')
    else:
        form = AddParentForm(instance=par)
    context = {
        "form": form,
    }
    template = 'hod_template/add_parent.html'
    return render(request, template, context)

@login_required
def delete_parent(request, pk):
    par = Parents.objects.get(id=pk)
    try:
        par.delete()
        messages.success(request, "Parent Deleted Successfully.")
        return redirect('school:manage_parent')
    except:
        messages.error(request, "Failed to Delete Parent.")
        return redirect('school:manage_parent')

@login_required
def manage_parent(request):
    parent_list = Parents.objects.all().order_by('-id')

    context = {
        'parent_list': parent_list,
    }

    template = 'hod_template/manage_parent.html'
    return render(request, template, context)

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
            request.session['id'] = student.id
            messages.success(request, "Student Added Successfully!")
            return redirect('school:add_student_education_history')
    else:
        form = AddStudentForm()


    context = {
        "form": form,

    }

    template = 'hod_template/add_student_template.html'
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

    template = 'hod_template/editstudent.html'
    return render(request, template, context)

@login_required
def manage_student(request):
    student_list = Students.objects.all().order_by('-id')

    context = {
        'student_list': student_list,
    }

    template = 'hod_template/manage_student.html'
    return render(request, template, context)

@login_required
def add_student_education(request):
    if request.session['id']:
        try:
            students = Students.objects.get(id = request.session['id'])
        except KeyError:
            pass
    else:
        messages.success(request, "Please Register a student")
        return redirect('school:add_student')

    if request.method == "POST":
        form = AddEducationForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.student_id = students
            student.save()

            messages.success(request, students.firstname + "'s" +
                             " " + "Educational History Added")
            return redirect('school:add_student_education_history')
    else:

        form = AddEducationForm()

    context = {
        "form": form,
        'students':students,

    }

    template = 'hod_template/student_education_history.html'
    return render(request, template, context)


@login_required
def add_student_emergency(request):
    if request.session['id']:
        try:
            students = Students.objects.get(id=request.session['id'])
        except KeyError:
            pass
    else:
        messages.success(request, "Please Register a student")
        return redirect('school:add_student')


    if request.method == "POST":
        form = EmmercencyForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.student_id = students
            student.save()

            messages.success(request, students.firstname+ "'s"+
                             " " + "Emmercency Contact Added")
            return redirect('school:add_student_emmergency_contact')
    else:

        form = EmmercencyForm()

    context = {
        "form": form,
        'students': students,

    }

    template = 'hod_template/emmercencycontact.html'
    return render(request, template, context)

@login_required
def add_student_medical(request):
    if request.session['id']:
        try:
            students = Students.objects.get(id=request.session['id'])
        except KeyError:
            pass
    else:
        messages.success(request, "Please Register a student")
        return redirect('school:add_student')


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
            return redirect('school:add_student_medical')
    else:

        form = MedicalForm()
        doc = DoctorForm(instance=students)

    context = {
        "form": form,
        'doc': doc,
        'students': students,
    }

    template = 'hod_template/medical.html'
    return render(request, template, context)

@login_required
def add_student_immunization(request):
    if request.session['id']:
        try:
            students = Students.objects.get(id=request.session['id'])
        except KeyError:
            pass
    else:
        messages.success(request, "Please Register a student")
        return redirect('school:add_student')

    if request.method == "POST":
        form = ImmunizationForm(request.POST)

        if form.is_valid():
            immune = form.save(commit=False)
            immune.student_id = students
            immune.save()

            messages.success(request, students.firstname + "'s" +
                             " " + "Immunization Added")
            return redirect('school:add_student_immunization')
    else:

        form = ImmunizationForm()

    context = {
        "form": form,
        'students': students,

    }

    template = 'hod_template/immunization.html'
    return render(request, template, context)

@login_required
def nexts(request):
    if request.session['id']:
        try:
            del request.session['id']
            return redirect('school:manage_student')
        except KeyError:
            return redirect('school:manage_student')

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

    template = 'hod_template/student_profile.html'

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
    template = 'hod_template/student_education_history.html'
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
    template = 'hod_template/emmercencycontact.html'
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
    template = 'hod_template/medicaledit.html'
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
    template = 'hod_template/immunization.html'
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
    template = 'hod_template/student_education_history.html'
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
    template = 'hod_template/emmercencycontact.html'
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
    template = 'hod_template/medicaledit.html'
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
    template = 'hod_template/immunization.html'
    return render(request, template, context)

@login_required
def add_staff(request):
    if request.method == "POST":
        form = AddStaffForm(request.POST, request.FILES)

        if form.is_valid():
            staff = form.save(commit=False)
            staff.staff_status ="Active"
            staff.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('school:add_staff_education_history', pk=staff.id)
    else:
        form = AddStaffForm()

    context = {
        "form": form,

    }

    template = 'hod_template/add_staff_template.html'
    return render(request, template, context)


@login_required
def add_staff_education(request,pk):

    try:
        staff = Staffs.objects.get(id=pk)

    except Staffs.DoesNotExist:
        messages.success(request, "Please Register a staff")
        return redirect('school:add_staff')
    staff_edu = StaffEducationHistory.objects.filter(staff_id=staff.id)
    if request.method == "POST":
        form = AddStaffEducationForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.staff_id = staff
            student.save()

            messages.success(request, staff.firstname + "'s" +
                             " " + "Educational History Added")
            return redirect('school:add_staff_education_history',pk=staff.id)
    else:

        form = AddStaffEducationForm()

    context = {
        "form": form,
        'students': staff,
        'staff_edu':staff_edu,

    }

    template = 'hod_template/staff_education_history.html'
    return render(request, template, context)

def remove_edu_history(request,pk):
    try:

        staff_edu = StaffEducationHistory.objects.get(id=pk)
        aa = staff_edu.staff_id
        staff_edu.delete()
        messages.success(request, "Education Removed")
        return redirect('school:add_staff_education_history' , aa)
    except StaffEducationHistory.DoesNotExist:
        messages.success(request, "Record Not Found")
        return redirect('school:add_staff_education_history' ,aa)

@login_required
def add_staff_work_experience(request,pk):
    try:
        staff = Staffs.objects.get(id=pk)
    except Staffs.DoesNotExist:
        messages.danger(request, "Please Register a staff")
        return redirect('school:add_staff')
    staff_wrk = StaffWorkExperience.objects.filter(staff_id=staff.id)
    for i in staff_wrk:
        print(i.company_name)

    if request.method == "POST":
        form = AddStaffWorkExperenceForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.staff_id = staff
            student.save()

            messages.success(request, staff.firstname + "'s" +
                             " " + "Work Experience Added")
            return redirect('school:add_staff_work_experience',pk=staff.id)
    else:

        form = AddStaffWorkExperenceForm()

    context = {
        "form": form,
        'students': staff,
        'staff_wrk':staff_wrk,
    }

    template = 'hod_template/work_experience.html'
    return render(request, template, context)

def remove_wrk_exp(request,pk):
    try:

        staff_edu = StaffWorkExperience.objects.get(id=pk)
        aa = staff_edu.staff_id
        staff_edu.delete()
        messages.success(request, "Work Experience Removed")
        return redirect('school:add_staff_work_experience' , aa)
    except StaffWorkExperience.DoesNotExist:
        messages.success(request, "Record Not Found")
        return redirect('school:add_staff_work_experience' ,aa)

@login_required
def add_staff_emmergency_contact(request,pk):
    try:
        staff = Staffs.objects.get(id=pk)
    except Staffs.DoesNotExist:
        messages.danger(request, "Please Register a staff")
        return redirect('school:add_staff')

    staff_cnt = StaffEmmergencyContacts.objects.filter(staff_id=staff.id)

    if request.method == "POST":
        form = StaffEmmercencyForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.staff_id = staff
            student.save()
            messages.success(request, staff.firstname + "'s" +
                             " " + "Emmergency Contact Added")
            return redirect('school:add_staff_emmergency_contact',pk=staff.id)
    else:

        form = StaffEmmercencyForm()

    context = {
        "form": form,
        'students': staff,
        'staff_cnt':staff_cnt,

    }

    template = 'hod_template/staffemmercencycontact.html'
    return render(request, template, context)


def remove_emm_con(request,pk):
    try:

        staff_edu = StaffEmmergencyContacts.objects.get(id=pk)
        aa = staff_edu.staff_id
        staff_edu.delete()
        messages.success(request, "Emmergency Contact Removed")
        return redirect('school:add_staff_emmergency_contact' , aa)
    except StaffEmmergencyContacts.DoesNotExist:
        messages.success(request, "Emmergency Contact Removed")
        return redirect('school:add_staff_emmergency_contact' ,aa)

@login_required
def staff_profile(request, pk):
    try:
        staff = Staffs.objects.get(id=pk)
    except Staffs.DoesNotExist:
        pass

    try:
        staff_education = StaffEducationHistory.objects.filter(staff_id=pk)
    except StaffEducationHistory.DoesNotExist:
        pass

    try:
        staff_emmergency_contact = StaffEmmergencyContacts.objects.filter(
            staff_id=pk)
    except StaffEmmergencyContacts.DoesNotExist:
        pass
    try:
        staff_working_history = StaffWorkExperience.objects.filter(
            staff_id=pk)
    except StaffWorkExperience.DoesNotExist:
        pass


    template = 'hod_template/staff_profile.html'

    context = {
        'students': staff,
        'student_education': staff_education,
        'student_emmergency_contact': staff_emmergency_contact,
        'student_work_history': staff_working_history,
    }

    return render(request, template, context)

def remove_staff(request,pk):
    try:

        staff_edu = Staffs.objects.get(id=pk)
        # u = User.objects.filter(username=staff_edu.id)
        # u.is_active=False
        # u.save()
        staff_edu.delete()
        messages.success(request, "Staff Deleted")
        return redirect('school:hrdashboard')
    except Staffs.DoesNotExist:
        messages.success(request, "Staff Deleted")
        return redirect('school:hrdashboard')


@login_required
def manage_staff(request):
    staff_list = Staffs.objects.all().order_by('-id')

    context = {
        'student_list': staff_list,
    }

    template = 'hod_template/manage_staff.html'
    return render(request, template, context)

@login_required
def edit_staff_education(request, pk):
    stuedu = StaffEducationHistory.objects.get(id=pk)
    staffdid = stuedu.staff_id_id

    staffs = Staffs.objects.get(id=staffdid)

    if request.method == "POST":
        form = AddStaffEducationForm(request.POST, instance=stuedu)

        if form.is_valid():
            parent = form.save()
            messages.success(request, "Educational History Updated!")
            return redirect('school:staff_profile', pk=staffs.id)
    else:
        form = AddStaffEducationForm(instance=stuedu)
    context = {
        "form": form,
        'students': staffs
    }
    template = 'hod_template/staff_education_history.html'
    return render(request, template, context)


@login_required
def edit_staff_emmergency(request, pk):
    stuedu = StaffEmmergencyContacts.objects.get(id=pk)
    staffdid = stuedu.staff_id_id

    staffs = Staffs.objects.get(id=staffdid)

    if request.method == "POST":
        form = StaffEmmercencyForm(request.POST, instance=stuedu)

        if form.is_valid():
            parent = form.save()
            messages.success(request, "Emmergency Contact Updated!")
            return redirect('school:staff_profile', pk=staffs.id)
    else:
        form = StaffEmmercencyForm(instance=stuedu)
    context = {
        "form": form,
        'students': staffs
    }
    template = 'hod_template/staffemmercencycontact.html'
    return render(request, template, context)

@login_required
def edit_staff_work(request, pk):
    stuedu = StaffWorkExperience.objects.get(id=pk)
    staffdid = stuedu.staff_id_id

    staffs = Staffs.objects.get(id=staffdid)

    if request.method == "POST":
        form = AddStaffWorkExperenceForm(request.POST, instance=stuedu)

        if form.is_valid():
            parent = form.save()
            messages.success(request, "Emmergency Contact Updated!")
            return redirect('school:staff_profile', pk=staffs.id)
    else:
        form = AddStaffWorkExperenceForm(instance=stuedu)
    context = {
        "form": form,
        'students': staffs
    }
    template = 'hod_template/work_experience.html'
    return render(request, template, context)

@login_required
def delete_staff_education(request, pk):
    par = StaffEducationHistory.objects.get(id=pk)
    studid = par.staff_id_id

    students = Staffs.objects.get(id=studid)
    try:
        stu = students.id
        par.delete()
        messages.success(request, "Educational History Deleted")
        return redirect('school:staff_profile', pk=stu)
    except:
        messages.error(request, "Failed to Delete Educational History.")
        return redirect('school:staff_profile', pk=stu)


@login_required
def delete_staff_emmergency(request, pk):
    par = StaffEmmergencyContacts.objects.get(id=pk)
    studid = par.staff_id_id

    students = Staffs.objects.get(id=studid)
    try:
        stu = students.id
        par.delete()
        messages.success(request, "Emmergency Contact Deleted")
        return redirect('school:staff_profile', pk=stu)
    except:
        messages.error(request, "Failed to Delete Emmergency Contact.")
        return redirect('school:staff_profile', pk=stu)

@login_required
def delete_staff_work(request, pk):
    par = StaffWorkExperience.objects.get(id=pk)
    studid = par.staff_id_id

    students = Staffs.objects.get(id=studid)
    try:
        stu = students.id
        par.delete()
        messages.success(request, "Work Experience Deleted")
        return redirect('school:staff_profile', pk=stu)
    except:
        messages.error(request, "Failed to Delete Work Experience.")
        return redirect('school:staff_profile', pk=stu)

@login_required
def add_profile_staff_education(request, pk):

    staffs = Staffs.objects.get(id=pk)

    if request.method == "POST":
        form = AddStaffEducationForm(request.POST)

        if form.is_valid():
            st = form.save(commit=False)
            st.staff_id = staffs
            st.save()
            messages.success(request, "Educational History Added!")
            return redirect('school:staff_profile', pk=staffs.id)
    else:
        form = AddStaffEducationForm()
    context = {
        "form": form,
        'students': staffs,
    }
    template = 'hod_template/staff_education_history.html'
    return render(request, template, context)


@login_required
def add_profile_staff_emmergency(request, pk):

    staffs = Staffs.objects.get(id=pk)

    if request.method == "POST":
        form = StaffEmmercencyForm(request.POST)

        if form.is_valid():
            st = form.save(commit=False)
            st.staff_id = staffs
            st.save()
            messages.success(request, "Emmergency Contact Added!")
            return redirect('school:staff_profile', pk=staffs.id)
    else:
        form = StaffEmmercencyForm()
    context = {
        "form": form,
        'students': staffs,
    }
    template = 'hod_template/staffemmercencycontact.html'
    return render(request, template, context)


@login_required
def add_profile_staff_work(request, pk):

    staffs = Staffs.objects.get(id=pk)

    if request.method == "POST":
        form = AddStaffWorkExperenceForm(request.POST)

        if form.is_valid():
            st = form.save(commit=False)
            st.staff_id = staffs
            st.save()
            messages.success(request, "Work Experience Added!")
            return redirect('school:staff_profile', pk=staffs.id)
    else:
        form = AddStaffWorkExperenceForm()
    context = {
        "form": form,
        'students': staffs,
    }
    template = 'hod_template/work_experience.html'
    return render(request, template, context)

@login_required
def edit_staff(request, pk):
    stud = Staffs.objects.get(id=pk)
    if request.method == "POST":
        form = AddStaffForm(request.POST, request.FILES, instance=stud)

        if form.is_valid():
            student = form.save()
            request.session['id'] = student.id
            messages.success(request, "Staff Record Updated")
            return redirect('school:staff_profile', pk=pk)
    else:
        form = AddStaffForm(instance=stud)

    context = {
        "form": form,

    }

    template = 'hod_template/add_staff_template.html'
    return render(request, template, context)

@login_required
def add_class(request):

    if request.method == "POST":
        form = AddClassForm(request.POST, request.FILES, )

        if form.is_valid():
            form.save()
            messages.success(request, "Class Added")
            return redirect('school:add_class')
    else:
        form = AddClassForm()

    context = {
        "form": form,

    }

    template = 'hod_template/add_class_template.html'
    return render(request, template, context)


@login_required
def edit_class(request,pk):
    clss = SchClass.objects.get(id=pk)
    if request.method == "POST":
        form = AddClassForm(request.POST, request.FILES, instance = clss )

        if form.is_valid():
            form.save()
            messages.success(request, "Class Updated")
            return redirect('school:manage_class')
    else:
        form = AddClassForm(instance=clss)

    context = {
        "form": form,

    }

    template = 'hod_template/add_class_template.html'
    return render(request, template, context)


@login_required
def manage_class(request):
    class_list = SchClass.objects.all().order_by('-id')

    context = {
        'class_list': class_list,
    }

    template = 'hod_template/manage_class.html'
    return render(request, template, context)


@login_required
def delete_class(request, pk):
    acad = SchClass.objects.get(id=pk)
    try:
        acad.delete()
        messages.success(request, "Class deleted")
        return redirect('school:manage_class')
    except:
        messages.error(request, "Failed to Delete Class.")
        return redirect('school:manage_class')


@login_required
def add_subject(request, pk):

    try:
        cls = SchClass.objects.get(pk=pk)
    except SchClass.DoesNotExist:
        pass

    if request.method == "POST":
        form = AddSubjectForm(request.POST, request.FILES, )

        if form.is_valid():
            sub = form.save(commit=False)
            sub.class_id = cls
            sub.save()
            messages.success(request, "Subject Added")
            return redirect('school:add_subject', pk= cls.id)
    else:
        form = AddSubjectForm()

    context = {
        "form": form,

    }
    template = 'hod_template/add_subject_template.html'
    return render(request, template, context)


@login_required
def edit_subject(request, pk):

    try:
        cls = Subjects.objects.get(pk=pk)
    except Subjects.DoesNotExist:
        pass

    if request.method == "POST":
        form = EditSubjectForm(request.POST, request.FILES, instance=cls )

        if form.is_valid():
            form.save()
            messages.success(request, "Subject Updated")
            return redirect('school:manage_subject')
    else:
        form = EditSubjectForm(instance=cls)

    context = {
        "form": form,

    }
    template = 'hod_template/edit_subject.html'
    return render(request, template, context)

@login_required
def delete_subject(request, pk):
    acad = Subjects.objects.get(id=pk)
    try:
        acad.delete()
        messages.success(request, "Subject deleted")
        return redirect('school:manage_subject')
    except:
        messages.error(request, "Failed to Delete Class.")
        return redirect('school:manage_manage_subject')


@login_required
def manage_subject(request):
    subject_list = Subjects.objects.all().order_by('-id')

    context = {
        'class_list': subject_list,
    }

    template = 'hod_template/manage_subject_template.html'
    return render(request, template, context)

@login_required
def create_bill(request):

    if request.method == "POST":
        form = AddBillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bill sucessfully created")
            return redirect('school:manage_bill')
        else:
            messages.warning(
                request, "Bill for this particular class has already been created. Please proceed to take run bill of the class")
            return redirect('school:manage_bill')

    else:
        form = AddBillForm()

    context = {
        'form': form,
    }

    template = 'hod_template/bill.html'
    return render(request, template, context)

@login_required
def manage_bill(request):
    bill = Bills.objects.all().order_by('-id')
    context = {
        'bill': bill,
    }
    template = 'hod_template/manage_bill.html'
    return render(request, template, context)

@login_required
def add_bill(request, pk):
    bill = Bills.objects.get(id=pk)
    if request.method == "POST":
        form = BillClassForm(request.POST)
        if form.is_valid():
            cc = form.save(commit=False)
            cc.bill_id = bill
            cc.class_id = bill.class_id
            cc.session_year_id = bill.session_year_id
            cc.term_year_id = bill.term_year_id
            cc.save()
            messages.success(request, "Class Bill Details Added")
            return redirect('school:add_bill',pk=bill.id)
    else:
        form=BillClassForm()

    context = {
        'form': form,
    }
    template = 'hod_template/classbill.html'
    return render(request, template, context)

@login_required
def view_bill(request, pk):
    bill = Bills.objects.get(id=pk)

    clsbill = Bills_class.objects.filter(
        bill_id=bill.id, session_year_id=bill.session_year_id, term_year_id=bill.term_year_id, class_id=bill.class_id)
    clsbill_total = clsbill.aggregate(cc=Sum('amount'))

    context = {
        'clsbill': clsbill,
        'clsbill_total': clsbill_total,
        'bill':bill,
    }
    template = 'hod_template/view_class_bill.html'
    return render(request, template, context)

@login_required
def generate_student_bill(request,pk):

    bill = Bills.objects.get(id=pk)
    clsbill = Bills_class.objects.filter(
        bill_id=bill.id, session_year_id=bill.session_year_id, term_year_id=bill.term_year_id, class_id=bill.class_id)
    clsbill_total = clsbill.aggregate(cc=Sum('amount'))
    try:
        stud = Students.objects.filter(course_id = bill.class_id)


    except Students.DoesNotExist:
        pass
    for s in stud:
           try:
                cc = StudentBill.objects.get(
                    student_id=s, session_year_id=bill.session_year_id, term_year_id=bill.term_year_id, bill_id=bill.id)

           except StudentBill.DoesNotExist:
               StudentBill.objects.create(
                   student_id=s, session_year_id=bill.session_year_id, term_year_id=bill.term_year_id, bill_id=bill.id, amount=clsbill_total['cc'], balance=clsbill_total['cc'], parent_id=s.parent_id)
    messages.success(request, "Bill Generated Successfully!")
    return redirect('school:view_bill', pk=bill.id)


@login_required
def create_payroll(request):

    if request.method == "POST":
        form = AddPayrollForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Payroll sucessfully created")
            return redirect('school:manage_payroll')
    else:
        form = AddPayrollForm()
    context = {
        'form': form,
    }

    template = 'hod_template/payroll.html'
    return render(request, template, context)


@login_required
def manage_payroll(request):
    pay = Payroll.objects.all().order_by('-id')
    context = {
        'pay': pay,
    }
    template = 'hod_template/manage_payroll.html'
    return render(request, template, context)

@login_required
def run_payroll(request):
    staff = Staffs.objects.filter(staff_status= "Active",salary__gt=0.00).order_by('-id')
    tot_salary = staff.aggregate(cc=Sum('salary'))
    acc_code = Account_code.objects.get(code = "Salary")
    pv= Pv.objects.create(description="Payment of Salary",amount=tot_salary['cc'],status="pending", account_code=acc_code)
    for st in staff:
        pvdetails =Pv_details.objects.create(pv=pv,description=st.Surname+" "+st.firstname, amount=st.salary)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # ,http_client=proxy_client
    for s in staff:
        try:

            message = client.messages.create(
                        to="+233" + s.phone,
                        from_=TWILIO_PHONE_NUMBER,
                        body="Dear" + " " + s.Surname +" "+ s.firstname + "," + " " + "your salary for this month is"+" " + str(s.salary) + ".Thank you ---- MULAN SMART SCHOOL MANAGEMENT SYSTEM")
        except IOError:
            print('fail')
            pass
    messages.success(request, "Generated Successfully")
    return redirect('school:manage_payroll')

@login_required
def manage_account_code(request):
    acc_code = Account_code.objects.all().order_by('-id')

    context = {
        'acc_code': acc_code,
    }
    template = 'hod_template/manage_accountcode.html'
    return render(request, template, context)

@login_required
def account_code(request):

    if request.method == "POST":
        form = AccountCodeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Code saved successfully")
            return redirect('school:manage_account_code')
    else:
        form = AccountCodeForm()

    context = {
        'form':form,
    }
    template = 'hod_template/account_code.html'
    return render(request, template, context)

@login_required
def editaccount_code(request,pk):
    acc_code = Account_code.objects.get(id=pk)
    if request.method == "POST":
        form = AccountCodeForm(request.POST,instance=acc_code)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Code Updated")
            return redirect('school:manage_account_code')
    else:
        form = AccountCodeForm(instance=acc_code)

    context = {
        'form': form,
    }
    template = 'hod_template/account_code.html'
    return render(request, template, context)

@login_required
def manage_pv(request):
    pv = Pv.objects.all().order_by('-id')

    context = {
        'pv': pv,
    }

    template = 'hod_template/manage_pv.html'
    return render(request, template, context)


@login_required
def create_pv(request):
    if request.method == "POST":
        form = PvForm(request.POST)
        if form.is_valid():
            cc= form.save(commit=False)
            cc.status ="pending"
            cc.save()
            messages.success(request, "Pv Created Successfully")
            return redirect('school:manage_pv')
    else:
        form = PvForm()

    context = {
        'form': form,
    }
    template = 'hod_template/create_pv.html'
    return render(request, template, context)

@login_required
def add_pv_details(request,pk):
    pvs = Pv.objects.get(id=pk)
    if request.method == "POST":
        form = PvDetailForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.pv =pvs
            cc.save()
            messages.success(request, "Pv details Added Successfully")
            return redirect('school:add_pv_details', pk=pvs.id)
    else:
        form = PvDetailForm()

    context = {
        'form': form,
    }
    template = 'hod_template/create_pvdetail.html'
    return render(request, template, context)

@login_required
def view_pv(request, pk):
    pvs = Pv.objects.get(id=pk)
    pvs_detail = Pv_details.objects.filter(pv=pvs.id)
    detail_total = pvs_detail.aggregate(cc=Sum('amount'))

    context = {
        'pvs':pvs,
        'pvs_detail':pvs_detail,
        'detail_total': detail_total,
        }
    template = 'hod_template/pv_details.html'
    return render(request, template, context)

def delete_pv(request, pk):
    pvs = Pv.objects.get(id=pk)
    pvs.delete()
    messages.success(request, "Pv Deleted")
    return redirect('school:manage_pv')

@login_required
def approve_pvs(request, pk):
    pvs = Pv.objects.get(id=pk)
    pvs.status = "approved"
    cc = pvs.save()
    st = Account_code.objects.get(code = pvs.account_code)
    Expenditure.objects.create(account_code=st, amount=pvs.amount, pvno = pvs)
    return redirect('school:view_pv', pk=pvs.id)

@login_required
def cancel_pvs(request, pk):
    pvs = Pv.objects.get(id=pk)
    pvs.status = "cancelled"
    pvs.save()
    return redirect('school:view_pv', pk=pvs.id)

@login_required
def allexpenses(request):
    today = datetime.datetime.now()
    ord = Expenditure.objects.all().order_by('-id')
    total = ord.aggregate(cc=Sum('amount'))

    myFilter = ExpenditureFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = myFilter.qs.aggregate(cc=Sum('amount'))

    template = 'hod_template/expenditureall.html'
    context = {
        'ord': ord,
        'total': total,
        'myFilter': myFilter,
    }
    return render(request, template, context)

@login_required
def allrevenue(request):
    today = datetime.datetime.now()
    ord = ARevenue.objects.all().order_by('-id')
    total = ord.aggregate(cc=Sum('amount'))

    myFilter = RevenueFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = myFilter.qs.aggregate(cc=Sum('amount'))

    template = 'hod_template/revenueall.html'
    context = {
        'ord': ord,
        'total': total,
        'myFilter': myFilter,
    }
    return render(request, template, context)

@login_required
def income_expenditure(request):
    today = datetime.datetime.now()
    ord = Expenditure.objects.filter(
        created_date__year=today.year).order_by('created_date')
    ords = Revenue.objects.filter(
        created_date__year=today.year).order_by('created_date')
    total = ord.aggregate(expense=Sum('amount'))
    tot = ords.aggregate(cc=Sum('amount'))
    if total['expense'] and tot['cc']:
        bf = tot['cc'] - total['expense']
    elif not total['expense'] and tot['cc']:
        bf = tot['cc']
    elif total['expense'] and not tot['cc']:
        bf = total['expense']
    elif not total['expense'] and not tot['cc']:
        bf = 0.00

    myFilter = ExpenditureFilter(request.GET, queryset=ord)
    myFilter2 = RevenueFilter(request.GET, queryset=ords)
    ord = myFilter.qs
    ords = myFilter2.qs
    total = myFilter.qs.aggregate(expense=Sum('amount'))
    tot = myFilter2.qs.aggregate(cc=Sum('amount'))
    if total['expense'] and tot['cc']:
        bf = tot['cc'] - total['expense']
    elif not total['expense'] and tot['cc']:
        bf = tot['cc']
    elif total['expense'] and not tot['cc']:
        bf = total['expense']
    elif not total['expense'] and not tot['cc']:
        bf = 0.00

    template = 'hod_template/monthlyincome.html'
    context = {
        'ord': ord,
        'ords': ords,
        'total': total,
        'tot': tot,
        'bf': bf,
        'myFilter': myFilter,
        'myFilter2': myFilter2,
    }
    return render(request, template, context)

@login_required
def stats_income_expenditure(request):
    acc= Account_code.objects.all()
    today = datetime.datetime.now()
    expenses = Expenditure.objects.values('account_code').annotate(
        month=TruncMonth('created_date'), monthly=Sum('amount')).order_by('month')
    income = Revenue.objects.values('account_code').annotate(
        month=TruncMonth('created_date'), monthly=Sum('amount')).order_by('month')
    ord = expenses
    ords = income
    total = Expenditure.objects.aggregate(expense=Sum('amount'))
    tot = Revenue.objects.aggregate(cc=Sum('amount'))
    if total['expense'] and tot['cc']:
        bf = tot['cc'] - total['expense']
    elif not total['expense'] and tot['cc']:
        bf = tot['cc']
    elif total['expense'] and not tot['cc']:
        bf = total['expense']
    elif not total['expense'] and not tot['cc']:
        bf = 0.00

    myFilter = ExpenditureFilter(request.GET, queryset=ord)
    myFilter2 = RevenueFilter(request.GET, queryset=ords)
    ord = myFilter.qs
    ords = myFilter2.qs
    total = ord.aggregate(expense=Sum('amount'))
    tot = ords.aggregate(cc=Sum('amount'))

    if total['expense'] and tot['cc']:
        bf = tot['cc'] - total['expense']
    elif not total['expense'] and tot['cc']:
        bf = tot['cc']
    elif total['expense'] and not tot['cc']:
        bf = total['expense']
    elif not total['expense'] and not tot['cc']:
        bf = 0.00

    template = 'hod_template/yearly.html'
    context = {
        'ord': ord,
        'ords': ords,
        'total': total,
        'tot': tot,
        'bf': bf,
        'myFilter': myFilter,
        'myFilter2': myFilter2,
        'acc': acc,
    }
    return render(request, template, context)

@login_required
def manage_fees(request):

    ord = StudentBill.objects.all().order_by('-id')
    total = StudentBill.objects.all().aggregate(cc=Sum('balance'))

    myFilter = StudentBillFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = myFilter.qs.aggregate(cc=Sum('balance'))
    template = 'hod_template/receive.html'
    context = {
        'ord': ord,
        'total': total,
        'myFilter': myFilter
    }
    return render(request, template, context)

@login_required
def account_receivable(request):

    ord = StudentBill.objects.filter(
        balance__gt=0.00).order_by('-id')
    total = StudentBill.objects.all().aggregate(cc=Sum('balance'))

    myFilter = AccountRecievableFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = myFilter.qs.aggregate(cc=Sum('balance'))
    template = 'hod_template/rec.html'
    context = {
        'ord': ord,
        'total': total,
        'myFilter': myFilter
    }
    return render(request, template, context)

@login_required
def make_payment(request, pk):
    st = StudentBill.objects.get(id=pk)
    if request.method == "POST":
        form = paymentform(request.POST)
        if form.is_valid():
            amount_paid = form.cleaned_data['amount_paid']
            paidby = form.cleaned_data['paidby']
            phone = form.cleaned_data['phone']
            st.amount_paid = float(st.amount_paid) + float(amount_paid)
            st.paidby = paidby
            st.paidbyphone = phone
            st.balance = float(st.amount) - float(st.amount_paid)
            st.save()
            acc = Account_code.objects.get(code="Fees")
            company = Company_group.objects.get(name="Mulan")
            Revenue.objects.create(
                account_code=acc, amount=st.amount_paid, stubill = st, company=company)
            messages.success(request, "Payment Made Successfully")
            return redirect('school:manage_fees')
    else:
        form = paymentform()

    context = {
        'form': form,
    }
    template = 'hod_template/payment.html'
    return render(request, template, context)

@login_required
def broadcast(request):
    if request.method == "POST":
        form = SmsForm(request.POST)
        if form.is_valid():
            sms = form.save()
            newsms = strip_tags(sms.sms)
            print(sms)
            par = Parents.objects.all()
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            # ,http_client=proxy_client
            for p in par:
                try:
                    message = client.messages.create(
                        to="+233" + p.father_phone,
                        from_=TWILIO_PHONE_NUMBER,
                        body="Dear" + " " + p.father_name + ",\n" +  newsms + "\n\nDATE:-28 June - 10 September \n" +
                        "VENUE: - Adjiringanor gate-near the Allied Petrol station." +
                        "TIME: - 7am - 5pm(Monday-Saturday)\n" +
                        "TEL: - 0207771025/0591439673\n" +
                        "FREE BREAKFAST & LUNCH.\n\n"+
                        "Limited vacancies available due to Covid and all Covid protocols shall be observed.")
                    message = client.messages.create(
                        to="+233" + p.mother_phone,
                        from_=TWILIO_PHONE_NUMBER,
                        body="Dear" + " " + p.mother_name + "," + " " + newsms)
                except IOError:
                    pass
            messages.info(request, 'Broadcast Sent')
    else:
        form =SmsForm()

    context = {
        'form': form,
    }
    template = 'hod_template/sms.html'
    return render(request, template, context)


@login_required
def manage_sms(request):
    sms = SMS.objects.all().order_by('-id')

    context = {
        'sms': sms,
    }

    template = 'hod_template/managesms.html'
    return render(request, template, context)

@login_required
def dashboard(request):
    all_student_count = Students.objects.all().count()
    course_count = SchClass.objects.all().count()
    staff_count = Staffs.objects.all().count()
    parent_count = Parents.objects.all().count()
    male_student = Students.objects.filter(gender ="Male").count()
    female_students = Students.objects.filter(gender="Female").count()
    student_list = Students.objects.all()
    active_students = Students.objects.filter(stu_status="Active").count()
    Inactive_students = Students.objects.filter(stu_status="Inactive").count()
    staff_list = Staffs.objects.all()

    context ={
        'all_student_count': all_student_count,
        'course_count': course_count,
        'staff_count': staff_count,
        'parent_count':parent_count,
        'male_student': male_student,
        'female_students':female_students,
        'student_list': student_list,
        'active_students': active_students,
        'Inactive_students':Inactive_students,
        'staff_list': staff_list,

    }
    template = 'hod_template/Dashboard.html'
    return render(request, template,context)

@login_required
def hrdashboard(request):
    all_student_count = Students.objects.all().count()
    course_count = SchClass.objects.all().count()
    staff_count = Staffs.objects.all().count()
    parent_count = Parents.objects.all().count()
    male_student = Students.objects.filter(gender ="Male").count()
    female_students = Students.objects.filter(gender="Female").count()
    student_list = Students.objects.all()
    active_students = Students.objects.filter(stu_status="Active").count()
    Inactive_students = Students.objects.filter(stu_status="Inactive").count()
    staff_list = Staffs.objects.all()
    myFilter = StaffFilter(request.GET, queryset=staff_list)
    staff_list = myFilter.qs
    context ={
        'all_student_count': all_student_count,
        'course_count': course_count,
        'staff_count': staff_count,
        'parent_count':parent_count,
        'male_student': male_student,
        'female_students':female_students,
        'student_list': student_list,
        'active_students': active_students,
        'Inactive_students':Inactive_students,
        'staff_list': staff_list,
        'myFilter':myFilter,

    }
    template = 'hod_template/hr.html'
    return render(request, template,context)

@login_required
def reminders(request):
    ord = StudentBill.objects.filter(
        balance__gt=0.00).order_by('-id')

    for b in ord:
        par = Parents.objects.get(id=b.parent_id)
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # ,http_client=proxy_client
        try:
            message = client.messages.create(
                        to="+233" + par.father_phone,
                        from_=TWILIO_PHONE_NUMBER,
                body="Dear" + " " + par.father_name + "," + " " + " A kindly reminder to pay the remaining bill of " + " " + str(b.balance) + " " + "of your ward" + " " + b.student_id.Surname + " " + b.student_id.firstname)
            message = client.messages.create(
                        to="+233" + par.mother_phone,
                        from_=TWILIO_PHONE_NUMBER,
                body="Dear" + " " + par.mother_name + "," + " " + " A kindly reminder to pay the remaining bill of " + " " + str(b.balance) + " " + "of your ward" + " " + b.student_id.Surname + " " + b.student_id.firstname)
        except IOError:
            pass
    messages.info(request,"Reminder Sent Succesfully")
    return redirect('school:accountreceivable')


def load_term(request):
    academic_year = request.GET.get('academicyear')
    terms = SessionTermModel.objects.filter(
        acadamic_year=academic_year)
    return render(request, 'hod_template/term.html', {'terms': terms})

@login_required
def manage_report(request):
    today = datetime.datetime.now()
    report = DailyClassReport.objects.filter(report_date =today).order_by('-id')
    template = 'hod_template/manage_dailyreport.html'
    context = {
        'report':report,
    }
    return render(request, template, context)

@login_required
def create_report(request):
    if request.method == "POST":
        form=DailyReportForm(request.POST)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            academic_year = form.cleaned_data['session_year_id']
            academic_term = form.cleaned_data['term_year_id']
            subjects = Subjects.objects.filter(class_id=class_id)
            for subject in subjects:
                DailyClassReport.objects.create(
                    class_id=class_id, subject=subject, session_year_id=academic_year, term_year_id = academic_term)
            messages.success(request, "Daily subject Report created Successfully")
            return redirect('school:manage_report')
    else:
        form= DailyReportForm()
    template = 'hod_template/create_dailyreport.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

@login_required
def list_students(request, pk):
    daily =DailyClassReport.objects.get(id=pk)
    students = Students.objects.filter(course_id = daily.class_id)
    request.session['id'] = daily.id

    template = 'hod_template/manage_daily_student_report.html'
    context = {
        'students': students,
    }
    return render(request, template, context)

@login_required
def dailyfinish(request):
    if request.session['id']:
        try:
            del request.session['id']
            if request.user.profile.is_staff:
                return redirect('school:manage_dailyreport')
            else:
                return redirect('school:manage_report')

        except KeyError:
            if request.user.profile.is_staff:
                return redirect('school:manage_dailyreport')
            else:
                return redirect('school:manage_report')

@login_required
def add_remarks(request, pk):
    students = Students.objects.get(id=pk)
    staffid = request.user.username
    staff = Staffs.objects.get(id=staffid)
    if request.session['id']:
        try:
            dailyreport = DailyClassReport.objects.get(id = request.session['id'])
        except DailyClassReport.DoesNotExist:
            pass

    if request.method == "POST":
        form = DailyClassReportDetailsForm(request.POST,request.FILES)
        if form.is_valid():
            DailyClassReportDetails.objects.create(class_id=students.course_id, session_year_id=dailyreport.session_year_id, term_year_id=dailyreport.term_year_id, student_id=students, parent_id=students.parent_id,
                                                   subject=dailyreport.subject, topic=form.cleaned_data['topic'], remarks=form.cleaned_data['remarks'], proof=form.cleaned_data['proof'], status="pending", teacher_id=staff, report_id=dailyreport)

            messages.success(
                request, "Topic Remarks of student added sucessfully")
            return redirect('school:list_students' , pk = dailyreport.id)

    else:
        form = DailyClassReportDetailsForm()
    template = 'hod_template/create_remarks.html'
    context = {
        'form': form,
    }


    return render(request, template, context)

@login_required
def dailyreport(request):
    rep =DailyClassReportDetails.objects.all().order_by('-id')
    template = 'hod_template/view_dailyreport.html'
    context ={
        'rep': rep,
    }
    return render(request, template, context)

@login_required
def view_student_daily_report(request,pk):
    rep = DailyClassReportDetails.objects.get(id=pk)
    student = Students.objects.get(id=rep.student_id)
    template = 'hod_template/dailyreport.html'
    context = {
        'rep': rep,
        'student':student,
    }
    return render(request, template, context)

@login_required
def approve_remarks(request, pk):
    rep = DailyClassReportDetails.objects.get(id=pk)
    rep.status = "approved"
    rep.save()
    messages.success(request, "Daily remarks approved")
    return redirect('school:view_student_daily_report',pk=rep.id)

@login_required
def delete_daily_report(request, pk):
    daily = DailyClassReport.objects.get(id=pk)
    daily.delete()
    messages.success(request, "Daily Report deleted")
    return redirect('school:manage_report')

@login_required
def manages_generalreport(request):
    genrep = GeneralClassReport.objects.all()
    template = 'staff_template/staff_manage_general.html'
    context ={
        'genrep': genrep,
    }
    return render(request, template, context)

@login_required
def view_general_report(request, pk):
    reps =GeneralClassReport.objects.get(id=pk)
    form = EditGeneralClassReportForm(instance=reps)
    template = 'hod_template/view_general_rep.html'
    context = {
        'reps': reps,
        'form': form,
    }
    return render(request, template, context)

@login_required
def approval_general_report(request, pk):
    genrep = GeneralClassReport.objects.get(id=pk)
    genrep.status ="approved"
    genrep.save()
    messages.success(request, "General Report approved")
    return redirect('school:manages_generalreport')

@login_required
def delete_general_report(request, pk):
    genrep = GeneralClassReport.objects.get(id=pk)
    genrep.delete()
    messages.success(request, "General Report deleted")
    return redirect('school:manages_generalreport')

def summer_contack(request):
    if request.method == "POST":
        form = TakeContact(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contact Added")
            return redirect('school:manage_contact')
    else:
        form = TakeContact()
    context = {
        'form': form,
    }
    template = 'hod_template/contact.html'
    return render(request, template, context)


def edit_summer_contack(request,pk):
    instance = Bulksend.objects.get(id=pk)
    if request.method == "POST":
        form = TakeContact(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request,"Contact Added")
            return redirect('school:manage_contact')
    else:
        form = TakeContact(instance=instance)
    context = {
        'form': form,
    }
    template = 'hod_template/contact.html'
    return render(request, template, context)

def manage_contact(request):
    contact =  Bulksend.objects.all()

    context = {
        'contact': contact,
    }
    template = 'hod_template/managecontact.html'
    return render(request, template, context)

def sendbroadcast(request):
    contact = Bulksend.objects.all()
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for c in contact:

        try:
            message = client.messages.create(
            to="+233" + c.phone,
            from_=TWILIO_PHONE_NUMBER,
            body="Dear" + " " + c.fathername + ","+"\nMulan Smart Activity Center brings you the best summer program, comprising of academic support and some special extra curriculum activities for kids between 6months- 12years.\n\n" +
            "DATE:-28 June - 10 September \n" +
            "VENUE: - Adjiringanor gate-near the Allied Petrol station." +
            "TIME: - 7am - 5pm(Monday-Saturday)\n" +
            "TEL: - 0207771025/0591439673\n" +
            "FREE BREAKFAST & LUNCH.\n\n"+
            "Limited vacancies available due to Covid and all Covid protocols shall be observed.")
        except IOError:
            print('fail')
            pass
    messages.success(request, 'Broadcast Sucessfully')
    return redirect('school:manage_contact')


def group_sms(request):
    if request.method == "POST":
        form = Group_smss(request.POST)
        if form.is_valid():
            cc=form.save()
            request.session['id'] = cc.batchno
            messages.success(request,"Please Proceed to add students to Batch Message")
            return redirect('school:managebatch')
    else:
        form = Group_smss()

    template = 'hod_template/batch.html'

    context = {
        'form': form,
    }
    return render(request, template, context)


def add_members(request, pk):

    smsgroup = Group_sms.objects.get(batchno=pk)
    smsstudents = Group_Sms_Student.objects.filter(batch_id=pk)
    student_list = Students.objects.all()

    request.session['id'] = smsgroup.batchno


    template = 'hod_template/add_studbatch.html'

    context = {
        'smsgroup':smsgroup,
        'smsstudents':smsstudents,
        'student_list':student_list,

    }

    return render(request, template, context)


def add_student_to_batch(request, pk):
    if request.session['id']:
        batchid = request.session['id']
        smsgroup = Group_sms.objects.get(batchno=batchid)
    Student = Students.objects.get(id=pk)
    Group_Sms_Student.objects.create(
            student_id = Student,
            batch_id=smsgroup
        )

    messages.success(request, "Student Added To Broadcast")
    return redirect('school:add_members', pk= smsgroup.batchno)

def studremove(request, pk):
    cc = Group_Sms_Student.objects.get(id=pk)
    cc.delete()

    messages.success(request, "Student Removed")
    return redirect('school:add_members', pk=request.session['id'])

def groupstudsend(request):
    if request.session['id']:
        cc = request.session['id']
        print(cc)
        # batchid = request.session['id']
        smsgroup = Group_sms.objects.get(batchno=cc)
        print(smsgroup.batchno)
        mes = strip_tags(smsgroup.batch_description)
        smsstudents = Group_Sms_Student.objects.filter(batch_id=cc)
        for b in smsstudents:
            print(b.student_id)
        # sid = smsstudents.student_id
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for stud in smsstudents:
            Student = Students.objects.get(id=stud.student_id)
            print(Student)
            fphone = Student.parent_id.father_phone
            fname = Student.parent_id.father_name
            mphone = Student.parent_id.mother_phone
            mname = Student.parent_id.mother_name
            try:
                message = client.messages.create(
                    to="+233" + fphone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear" + " " + fname + ",\n"+ mes
                    )
            except IOError:
                print('fail')
                pass
            try:
                message = client.messages.create(
                    to="+233" + mphone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear" + " " + mname + ",\n" + mes
                    )
            except IOError:
                print('fail')
                pass
        messages.success(request, 'Broadcast Sucessfully')
        return redirect('school:add_members', pk=cc)

def done(request):
    if request.session['id']:
        try:
            del request.session['id']
            return redirect('school:managebatch')
        except KeyError:
            return redirect('school:managebatch')



def managebatch(request):
    mes = Group_sms.objects.all().order_by('-batchno')

    template = 'hod_template/managebatch.html'
    context = {
        'mes': mes
        }
    return render(request, template, context)



def upload_hr_report(request):

    if request.method == "POST":
        form = HrReportForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save()
            messages.success(request, "Report Uploaded!")
            return redirect('school:managereports')
    else:
        form = HrReportForm()


    context = {
        "form": form,

    }

    template = 'hod_template/hr_report.html'
    return render(request, template, context)


def managereports(request):
    mes = Hr_reports.objects.all().order_by('-id')

    template = 'hod_template/manage_reports.html'
    context = {
        'mes': mes
        }
    return render(request, template, context)






