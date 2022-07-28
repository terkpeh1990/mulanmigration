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
from django.contrib.auth.decorators import login_required


def manage_subjects(request):
    subjects = Subjects.objects.all()
    
   

    if request.method =='POST':
        form=AddSubjectForm(request.POST)
        
        if form.is_valid():
            form.save()
           
            messages.success(request,"Subject Saved")
            return redirect('school:manage_subjects')
    else:
        form = AddSubjectForm()
  
    template = 'subjects/manage_subjects.html'
    context={
        'subjects':subjects,
        
        'form':form,
    }
    return render(request,template,context)


def edit_subjects(request,pk):
    subjects = Subjects.objects.all()
    subject = subjects.get(id=pk)
    
   

    if request.method =='POST':
        form=AddSubjectForm(request.POST,instance=subject)
        
        if form.is_valid():
            form.save()
           
            messages.success(request,"Subject Updated")
            return redirect('school:manage_subjects')
    else:
        form = AddSubjectForm(instance=subject)
  
    template = 'subjects/manage_subjects.html'
    context={
        'subjects':subjects,
        
        'form':form,
    }
    return render(request,template,context)



def assign_subject_to_class(request,pk):
    schclass = SchClass.objects.get(id=pk)
    ass_classes = SchClass_Subjects.objects.filter(class_id=schclass.id).order_by('-id')
    if request.method == "POST":
        form = AddSubjecttoclassForm(request.POST)

        if form.is_valid():
            sub = form.cleaned_data['subject_id']
            subject = Subjects.objects.get(id=sub.id)
            if SchClass_Subjects.objects.filter(class_id=schclass.id,subject_id=subject.id).exists():
                messages.success(
                    request, "Subject Already Selected")
                return redirect('school:assign_subject_to_class' ,schclass.id)
            else:
                cc=form.save(commit=False)
                cc.class_id=schclass
                cc.save()
            
                messages.success(
                        request, "Subject Assigned Successfully")
                return redirect('school:assign_subject_to_class' ,schclass.id)
    else:
        form = AddSubjecttoclassForm()

    context = {
        "form": form,
        'schclass':schclass,
        'ass_classes':ass_classes,
    }
    template = 'subjects/assign_subject.html'
    return render(request, template, context)



def remove_stubject(request,pk):
    ass_classes = SchClass_Subjects.objects.get(id=pk)
    cc = ass_classes.class_id.id
    ass_classes.delete()
    messages.success(request ,'Subject Removed')
    return redirect('school:assign_subject_to_class',cc)
    
