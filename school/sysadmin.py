from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .filters import *
# from .utils import randompassword
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import Group



def manage_profiles(request):
    profile = Profile.objects.all()

    template = 'sysadmin/manage_profile.html'
    context ={
        'profile':profile,
        
    }
    return render(request,template,context)


def reset_staff_password(request,pk):
    profile = Profile.objects.get(id=pk)
    cc = "password@12345"
    password = make_password(cc)
    staff = profile.user
    staff.password=password
    staff.save()
    profile.is_new = True
    profile.save()
    messages.success(request,'Password Reset Successful')
    return redirect('school:manage_profiles')

@login_required
def populate_grouping(request):
    gr=Group.objects.all()
    for i in gr:
        Grouping_name.objects.create(name=i.name)
    messages.success(request,'User Group populated')
    return redirect('school:manage_grouping')

def delete_grouping(request):
    gr=Grouping_name.objects.all()
    for i in gr:
        i.delete()
    messages.success(request,'User Group deleted')
    return redirect('school:manage_grouping')

    
def manage_grouping(request):
    profile = Grouping_name.objects.all()
    template = 'sysadmin/manage_grouping.html'
    context ={
        'profile':profile,
    }
    return render(request,template,context)

def assign_grouping(request,pk):
    profile = Profile.objects.get(id=pk)
    usergroup = Grouping_name.objects.all()
    template = 'sysadmin/assign_grouping.html'
    context ={
        'profile':profile,
        'usergroup':usergroup,
    }
    return render(request,template,context)

def make_inactive(request,pk):
    profile = Profile.objects.get(id=pk)
    profile.user.delete()
    messages.success(request,'Staff Has been made Inactive on the system')
    return redirect('school:manage_profiles')

def set_staff_group(request,profileid,groups):
    profile = Profile.objects.get(id=profileid)
    profile.is_staff = False
    profile.is_hr = False
    profile.is_admin = False
    profile.is_principal = False
    profile.is_parent = False
    profile.is_manager = False
    profile.is_account = False
    profile.is_bakery = False
    profile.is_partytree = False
    profile.is_irishgreen = False
    usergroup = Grouping_name.objects.get(id=groups)
    gg = Group.objects.get(name=usergroup.name)
    profile.user.groups.clear()
    profile.user.groups.add(gg)
    if usergroup.name == 'hr':
        profile.is_hr = True
    elif usergroup.name == 'admin':
        profile.is_admin = True

    elif usergroup.name == 'teacher':
        profile.is_staff = True
    elif usergroup.name == 'principal':
        profile.is_principal = True
    elif usergroup.name == 'parent':
            profile.is_parent = True
    elif usergroup.name == 'manager':
            profile.is_manager = True
    elif usergroup.name == 'account':
            profile.is_account = True
    elif usergroup.name == 'bakerysupervisor' or usergroup.name == 'bakerykitchen' or usergroup.name == 'bakerycashier' :
            profile.is_bakery = True
    elif usergroup.name == 'partytreecashier' or usergroup.name == 'partytreesupervisor'  :
            profile.is_partytree = True
    else:
        profile.is_irishgreen = True
   
    profile.save()
    messages.success(request,'User Group assigned  Successful')
    return redirect('school:assign_grouping',pk=profile.id)