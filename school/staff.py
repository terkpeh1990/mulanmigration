from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from .forms import *
from .models import *
from django.db.models import  F
from django.db.models.expressions import Window
from django.db.models.functions import Rank


@login_required
def create_attendance(request):
    if request.method == "POST":
        form = AddAttendance(request.POST)

        if form.is_valid():
            sub = form.save()
            messages.success(
                request, "Attendance Created, Now proceed to take attendance")
            return redirect('school:manage_attendance')
        else:
            messages.warning(
                request, "Attendance for this particular class has already been created. Please proceed to take the attendance of the class")
            return redirect('school:manage_attendance')
    else:
        form = AddAttendance()


    context = {
        "form": form,

    }
    template = 'staff_template/create_attendance.html'
    return render(request, template, context)


@login_required
def manage_attendance(request):
    today = datetime.datetime.now()
    attendance_list = Attendance.objects.filter(attendance_date__month= today.month
        ).order_by('-id')
    context = {
        'academic_term': attendance_list,
    }

    template = 'staff_template/manage_attendance.html'
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
def edit_attendance(request,pk):
    try:
        attendance = Attendance.objects.get(id=pk)
    except Attendance.DoesNotExist:
        pass
    if request.method == "POST":
        form = AddAttendance(request.POST, instance=attendance)

        if form.is_valid():
            today = datetime.date.today()
            acadyear = SessionYearModel.objects.get(status='Active')
            acadterm = SessionTermModel.objects.get(status='Active')

            sub = form.save(commit=False)
            sub.session_year_id = acadyear
            sub.term_year_id = acadterm
            sub.save()
            messages.success(
                request, "Attendance Created, Now proceed to take attendance")
            return redirect('school:manage_attendance')
    else:
        form = AddAttendance(instance=attendance)

    context = {
        "form": form,

    }
    template = 'staff_template/create_attendance.html'
    return render(request, template, context)


@login_required
def take_attendance(request, pk):

    attendance = Attendance.objects.get(id=pk)
    stu = Students.objects.filter(course_id=attendance.class_id, att=False)


    request.session['attend'] = attendance.id
    context = {
        'stu': stu,

    }
    template = 'staff_template/take_attendance.html'
    return render(request, template, context)


@login_required
def present(request,pk):
    stu = Students.objects.get(id=pk)
    if request.session['attend']:
        attendid = request.session['attend']
        att = Attendance.objects.get(id = attendid)
        AttendanceReport.objects.create(student_id=stu, attendance_id=att, status=True)
        stu.att = True
        stu.save()
        return redirect('school:take_attendance', pk=attendid)


@login_required
def absent(request, pk):
    stu = Students.objects.get(id=pk)
    if request.session['attend']:
        attendid = request.session['attend']
        att = Attendance.objects.get(id=attendid)
        AttendanceReport.objects.create(student_id=stu, attendance_id=att, status=False)
        stu.att = True
        stu.save()
        return redirect('school:take_attendance', pk=attendid)


@login_required
def closing(request):
    stu = Students.objects.all()
    if request.session['attend']:
        del request.session['attend']
        for s in stu:
            s.att = False
            s.save()
        return redirect('school:manage_attendance')


@login_required
def view_attendance(request,pk):

    stu = AttendanceReport.objects.filter(attendance_id=pk)
    context = {
        'stu': stu,
    }
    template = 'staff_template/view_attendance.html'
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
def create_results(request):
    if request.method == "POST":
        form = AddResults(request.POST)

        if form.is_valid():
            today = datetime.date.today()
            acadyear = SessionYearModel.objects.get(status='Active')
            acadterm = SessionTermModel.objects.get(status='Active')

            sub = form.save(commit=False)
            sub.session_year_id = acadyear
            sub.term_year_id = acadterm
            sub.results_date = today
            sub.save()
            messages.success(
                request, "Terminal results Created")
            return redirect('school:manage_results')
    else:
        form = AddResults()

    context = {
        "form": form,

    }
    template = 'staff_template/create_results.html'
    return render(request, template, context)


@login_required
def manage_results(request):
    today = datetime.datetime.now()
    attendance_list = Results.objects.filter(
        results_date__year=today.year).order_by('-id')
    context = {
        'academic_term': attendance_list,
    }

    template = 'staff_template/manage_results.html'
    return render(request, template, context)


@login_required
def delete_results(request, pk):
    acad = Results.objects.get(id=pk)
    try:
        acad.delete()
        messages.success(request, "Results deleted")
        return redirect('school:manage_results')
    except:
        messages.error(request, "Failed to Delete Results.")
        return redirect('school:manage_results')


@login_required
def edit_results(request, pk):
    try:
        attendance = Results.objects.get(id=pk)
    except Results.DoesNotExist:
        pass
    if request.method == "POST":
        form = AddResults(request.POST, instance=attendance)

        if form.is_valid():
            today = datetime.date.today()
            acadyear = SessionYearModel.objects.get(status='Active')
            acadterm = SessionTermModel.objects.get(status='Active')

            sub = form.save(commit=False)
            sub.session_year_id = acadyear
            sub.term_year_id = acadterm
            sub.results_date = today
            sub.save()
            messages.success(
                request, "Terminal Results Updated")
            return redirect('school:manage_results')
    else:
        form = AddResults(instance=attendance)

    context = {
        "form": form,

    }
    template = 'staff_template/create_results.html'
    return render(request, template, context)


@login_required
def add_results(request, pk):
    try:
        if request.session['resul']:
            del request.session['resul']
    except KeyError:
        pass

    res = Results.objects.get(id=pk)
    stu = Students.objects.filter(course_id=res.class_id, stu_check=False)
    stus = Students.objects.filter(course_id=res.class_id, stu_check=True)
    request.session['resul'] = res.id
    context = {
        'stu': stu,
        'stus':stus,
    }
    template = 'staff_template/take_results.html'
    return render(request, template, context)


@login_required
def subject_results(request, pk):
    try:
        if request.session['student']:
            ss = Students.objects.get(id = request.session['student'])
        else:
            pass
    except KeyError:
        ss = Students.objects.get(id =pk)

    subj = Subjects.objects.filter(class_id=ss.course_id)

    request.session['student'] = ss.id
    context = {
        'subj': subj,

    }
    template = 'staff_template/result_subject_list.html'
    return render(request, template, context)


@login_required
def create_student_results(request,pk):
    if request.method == "POST":
        form = AddStudentResults(request.POST)
        try:
            sub = Subjects.objects.get(id=pk)
        except Subjects.DoesNotExist:
            pass
        if request.session['resul']:
            re = Results.objects.get(id=request.session['resul'])
        else:
            re = None
        if request.session['student']:
            s = Students.objects.get(id = request.session['student'])
        else:
            s = None
        if form.is_valid():
            today = datetime.date.today()
            acadyear = SessionYearModel.objects.get(status='Active')
            acadterm = SessionTermModel.objects.get(status='Active')

            results = form.save(commit=False)
            results.session_year_id = acadyear
            results.term_year_id = acadterm
            results.results_id=re
            results.subject_id = sub
            results.student_id = s
            results.course_id = s.course_id
            results.save()

            messages.success(
                request, "Results Added")
            return redirect('school:subject_results', sub.class_id)
    else:
        form = AddStudentResults()

    context = {
        "form": form,

    }
    template = 'staff_template/add_results.html'
    return render(request, template, context)


@login_required
def resultclose(request):
    try:
        if request.session['student']:
            del request.session['student']
    except KeyError:
        pass
    if request.session['resul']:
        if request.user.profile.is_parent:
            return redirect('school:stud_results', pk=request.session['resul'])
        else:
            return redirect('school:add_results', pk=request.session['resul'])



@login_required
def view_student_result(request,pk):
    try:
        if request.session['resul']:
            resid = request.session['resul']
        else:
            resid = None
    except KeyError:
        pass


    student_results = StudentResult.objects.filter(student_id=pk, results_id =resid )


    studentss = Students.objects.get(id=pk)
    context = {
        'student_results': student_results,
        'studentss': studentss,


    }
    template = 'staff_template/students_results.html'
    return render(request,template,context)


@login_required
def studentresultclose(request):
    try:
        if request.session['student']:
            del request.session['student']
    except KeyError:
        pass
    if request.session['resul']:
        return redirect('school:add_results', pk=request.session['resul'])


@login_required
def add_promotion(request, pk):


    # res = Results.objects.get(id=pk)
    stu = Students.objects.get(id=pk)
    if request.method=="POST":
        form = AddPromotionForm(request.POST, instance=stu)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.att = False
            cc.stu_check = True
            cc.save()
            try:
                if request.session['resul']:
                    return redirect('school:add_results', pk=request.session['resul'])
            except KeyError:
                pass
    else:
        form = AddPromotionForm(instance=stu)



    # request.session['resul'] = res.id
    context = {
        'form':form,

    }
    template = 'staff_template/promo.html'
    return render(request, template, context)


@login_required
def staff_dashboard(request):
    staff = Staffs.objects.get(id=request.user.username)
    all_student_count = Students.objects.filter(course_id=staff.course_id).count()
    course_count = SchClass.objects.all().count()
    staff_count = Staffs.objects.all().count()
    parent_count = Parents.objects.all().count()
    student_list = Students.objects.filter(course_id=staff.course_id)
    male_student = student_list.filter(gender="Male").count()
    female_students = student_list.filter(gender="Female").count()
    active_students = student_list.filter(stu_status="Active").count()
    Inactive_students = student_list.filter(stu_status="Inactive").count()
    attendance_list = Attendance.objects.filter(class_id=staff.course_id)
    context = {
        'all_student_count': all_student_count,
        'course_count': course_count,
        'staff_count': course_count,
        'parent_count': parent_count,
        'male_student': male_student,
        'female_students': female_students,
        'student_list': student_list,
        'active_students': active_students,
        'Inactive_students': Inactive_students,
        'attendance_list': attendance_list,

    }
    template = 'staff_template/staffDashboard.html'
    return render(request, template, context)


def stud_results(request, pk):

    res = Results.objects.get(id=pk)
    par = Parents.objects.get(id = request.user.username)
    stu= Students.objects.filter(
        parent_id=par.id,course_id=res.class_id)

    request.session['resul'] = res.id
    context = {
        'stu': stu,

    }
    template = 'staff_template/take_results.html'
    return render(request, template, context)


def print_student_result(request, pk):
    try:
        if request.session['resul']:
            resid = request.session['resul']
        else:
            resid = None
    except KeyError:
        pass

    student_results = StudentResult.objects.filter(
        student_id=pk, results_id=resid)

    studentss = Students.objects.get(id=pk)
    context = {
        'student_results': student_results,
        'studentss': studentss,


    }
    template = 'staff_template/students_results-print.html'
    return render(request, template, context)


@login_required
def viewing_results(request):
    today = datetime.datetime.now()
    attendance_list = studenthistory.objects.all().order_by('-results')
    context = {
        'academic_term': attendance_list,
    }

    template = 'staff_template/manage_resultss.html'
    return render(request, template, context)


@login_required
def add_resultss(request, pk):
    try:
        if request.session['resul']:
            del request.session['resul']
    except KeyError:
        pass

    res = Results.objects.get(id=pk)
    stu = studenthistory.objects.filter(
        course_id=res.class_id)
    request.session['resul'] = res.id
    context = {
        'stu': stu,
    }
    template = 'staff_template/take_resultss.html'
    return render(request, template, context)


@login_required
def print_student_results(request, pk):
    studentss = studenthistory.objects.get(id=pk)
    student_results = StudentResult.objects.filter(
        student_id=studentss.studid, results_id=studentss.results)
    stus = Students.objects.get(id=studentss.studid)
    context = {
        'student_results': student_results,
        'studentss': studentss,
        'stus':stus,


    }
    template = 'staff_template/students_results-print.html'
    return render(request, template, context)


@login_required
def view_student_results(request, pk):
    studentss = studenthistory.objects.get(id=pk)
    student_results = StudentResult.objects.filter(
        student_id=studentss.studid, results_id=studentss.results)

    stus = Students.objects.get(id=studentss.studid)
    context = {
        'student_results': student_results,
        'studentss': studentss,
        'stus':stus,

    }
    template = 'staff_template/students_results.html'
    return render(request, template, context)


@login_required
def manage_dailyreport(request):
    today = datetime.datetime.now()
    staff = Staffs.objects.get(id = request.user.username)
    report = DailyClassReport.objects.filter(
        report_date=today, class_id=staff.course_id).order_by('-id')
    template = 'hod_template/manage_dailyreport.html'
    context = {
        'report': report,
    }
    return render(request, template, context)


@login_required
def staffdailyreport(request):
    rep = DailyClassReportDetails.objects.filter(teacher_id=request.user.username).order_by('-id')
    template = 'hod_template/view_dailyreport.html'
    context = {
        'rep': rep,
    }
    return render(request, template, context)


@login_required
def generalreport(request):
    if request.method == "POST":
        form = GeneralClassReportForm(request.POST)
        if form.is_valid():
           gen= form.save(commit=False)
           staff = Staffs.objects.get(id = request.user.username)
           gen.teacher_id = staff
           gen.status = "pending"
           gen.save()
           return redirect('school:manage_generalreport')

    else:
        form = GeneralClassReportForm()
    template = 'staff_template/create_generalreport.html'
    context ={
        'form': form,
    }
    return render(request, template, context)


@login_required
def manage_generalreport(request):
    genrep = GeneralClassReport.objects.filter(teacher_id=request.user.username)
    template = 'staff_template/staff_manage_general.html'
    context ={
        'genrep': genrep,
    }
    return render(request, template, context)
