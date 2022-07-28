from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            type_obj = Profile.objects.get(user=request.user.username)
            # type = request.user.profile
            if type_obj.is_admin:
                return redirect('school:dashboard')
            elif type_obj.is_staff:
                return redirect('school:staff_dashboard')
            elif type_obj.is_principal:
                return redirect('school:principaldashboard')
            elif type_obj.is_parent:
                return redirect('school:parentdashboard')
            else:
                return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator
