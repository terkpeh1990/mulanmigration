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
def add_academicyear(request):

    if request.method == "POST":
        form = AcademicYearForm(request.POST, request.FILES, )

        if form.is_valid():
            try:
                cha = SessionYearModel.objects.last()
            except SessionYearModel.DoesNotExist:
                pass
            if cha:
                cha.status = "Inactive"
                cha.save()
            cc= form.save()
            terms = Terms.objects.all()
            for a in terms:
                SessionTerm.objects.create(acadamic_years=cc,acadamic_terms=a)
            messages.success(request, "Academic Year Added")
            return redirect('school:manage_academicyear')
    else:
        form = AcademicYearForm()

    context = {
        "form": form,

    }

    template = 'academic_year/add_academicyear.html'
    return render(request, template, context)

@login_required
def manage_academicyear(request):
    academic_year_list = SessionYearModel.objects.all().order_by('-id')

    context = {
        'academic_year_list': academic_year_list,
    }

    template = 'academic_year/manage_academicyear.html'
    return render(request, template, context)

@login_required
def edit_academicyear(request,pk):
    acad = SessionYearModel.objects.get(pk=pk)
    if request.method == "POST":
        form = EdithAcademicYearForm(
            request.POST, request.FILES, instance=acad)

        if form.is_valid():
            form.save()
            messages.success(request, "Academic Year Updated")
            return redirect('school:manage_academicyear')
    else:
        form = EdithAcademicYearForm(instance=acad)

    context = {
        "form": form,

    }

    template = 'academic_year/add_academicyear.html'
    return render(request, template, context)

@login_required
def delete_academic_year(request, pk):
    acad = SessionYearModel.objects.get(id=pk)

    try:
        acad.delete()
        messages.success(request, "Academic Year deleted")
        return redirect('school:manage_academicyear')
    except:
        messages.error(request, "Failed to Delete Academic Year.")
        return redirect('school:manage_academicyear')



def manage_academicterm(request):
    academic_term = SessionTerm.objects.all().order_by('-id')

    context = {
        'academic_term': academic_term,
    }

    template = 'academic_year/manage_academicterm.html'
    return render(request, template, context)

def load_term(request):
    region_id = request.GET.get('region')
    print(region_id)
    district = SessionTerm.objects.filter(acadamic_years=region_id)
    for a in district:
        print(a.acadamic_terms.name)
    return render(request, 'academic_year/term_dropdown_list.html', {'district': district})