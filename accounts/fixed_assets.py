from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *


def manage_assets(request):
    payables = FixedAssets.objects.all()
    
   

    if request.method =='POST':
        form=Assetsform(request.POST)
        
        if form.is_valid():
            form.save()
           
            messages.success(request,"Fixed Assets Saved")
            return redirect('accounts:manage_assets')
    else:
        form = Assetsform()
  
    template = 'accounts/manage_assets.html'
    context={
        'payables':payables,
        
        'form':form,
    }
    return render(request,template,context)