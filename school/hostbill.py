from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .forms import *
from .models import *
from .filters import *
from twilio.rest import TwilioRestClient
from twilio.rest import Client
from school_management_system.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic.edit import CreateView
from django.core import serializers
from twilio.rest import Client



def create_host_bill(request):
    if request.method == 'POST':
        form = HostOrderForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('school:manage_hostbill')
    else:
        form = HostOrderForm()
    
    template = 'hosbill/createord.html'
    context ={
        'form': form,
    }
    return render(request, template, context)

def add_host_items(request, pk):
    hostord = HostOrder.objects.get(id=pk)
    details = HostOrder_Details.objects.filter(order_id=hostord)
    if request.method == 'POST':
        form = OrderdetailsForm(request.POST)
        if form.is_valid():
            cc =form.save(commit=False)
            cc.order_id = hostord
            cc.save()
            hostord.total_price += cc.unit_price
            hostord.save()
            return redirect('school:add_host_items', pk=hostord.id)
    else:
        form = OrderdetailsForm()
        
    template = 'hosbill/add_items.html'
    context ={
        'form':form,
        'details': details,
        'hostord': hostord,
    }
    return render(request, template, context)

def manage_hostbill(request):
    hostord = HostOrder.objects.all()
    template = 'hosbill/manage_hostbill.html'
    context = {
        'hostord': hostord
        }
    return render(request, template, context)


def list_hostbill(request):
    hostord = HostOrder.objects.filter(total_price__gt=0.00)
    template = 'hosbill/listhost_bill.html'
    context = {
        'hostord': hostord
    }
    return render(request, template, context)

def view_hostbill(request, pk):
    hostord = HostOrder.objects.get(id=pk)
    details = HostOrder_Details.objects.filter(order_id = hostord)
    template = 'hosbill/invoice.html'
    context ={
        'hostord': hostord,
        'details': details,
    }
    return render(request, template, context)


def print_hostbill(request, pk):
    hostord = HostOrder.objects.get(id=pk)
    details = HostOrder_Details.objects.filter(order_id=hostord)
    template = 'hosbill/invoice-print.html'
    context = {
        'hostord': hostord,
        'details': details,
    }
    return render(request, template, context)

def tex(request):
    return render(request,'hosbill/invoice.html')
