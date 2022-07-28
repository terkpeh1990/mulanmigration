from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *
from .filters import *
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .smsthread import NotificationThreads
from school_management_system.settings import endPoint,apiKey,mulan_sender_id
import requests

def broadcasts(request):
    if request.method == "POST":
        form = SmsNotificationForm(request.POST)
        if form.is_valid():
            sms = form.save()
            newsms = strip_tags(sms.sms)
            print(sms)
            students = Students.objects.filter(stu_status='Active')
            item =[]
            if sms.venue:
                item.append('Venue : '+sms.venue)
            if sms.event_date:
                item.append('Date : '+sms.event_date)
            if sms.event_time:
                item.append('Time : '+sms.event_time)
            if sms.phone:
                item.append('Tel : '+sms.phone)
            
        for i in students:
                
            try:
                body = [
                    'Dear '+i.parent_id.father_name,
                    '\n'+ newsms,
                    '\n'+'\n'.join(item),
                    
                ]
                m = body
                
                
                phone= i.parent_id.father_phone
                message =  "\n".join(m)
                sender_id= mulan_sender_id
                url = endPoint + '?key=' + apiKey 
                response = requests.post(url+'&to='+phone +'&msg='+message+'&sender_id='+sender_id)
                data = response.json()
                print(data)
            except IOError:
                Sms_errormesseage.objects.create(message=newsms,venue=sms.venue,event_time=sms.event_time,event_date=sms.event_date,recepient=i.parent_id.father_phone)
                pass
            try:
                body = [
                    'Dear '+i.parent_id.mother_name,
                    '\n'+ newsms,
                    '\n'.join(item),
                    
                ]
                m = body
                
                
                phone= i.parent_id.mother_phone
                message =  "\n".join(m)
                sender_id= mulan_sender_id
                url = endPoint + '?key=' + apiKey 
                response = requests.post(url+'&to='+phone +'&msg='+message+'&sender_id='+sender_id)
                data = response.json()
                print(data)
            except IOError:
                Sms_errormesseage.objects.create(message=newsms,venue=sms.venue,event_time=sms.event_time,event_date=sms.event_date,recepient=i.parent_id.father_phone)
                pass


            NotificationThreads(newsms,sms,students)
            messages.info(request,'Broadcast Started')
            return redirect('school:sms_notifications')
    else:
        form =SmsNotificationForm()

    context = {
        'form': form,
    }
    template = 'sms/sms.html'
    return render(request, template, context)


@login_required
def sms_notifications(request):
    sms = Sms_notification.objects.all().order_by('-id')

    context = {
        'sms': sms,
    }

    template = 'sms/managesms.html'
    return render(request, template, context)


def managebatchss(request):
    mes = Group_sms.objects.all().order_by('-batchno')

    template = 'sms/managebatch.html'
    context = {
        'mes': mes
        }
    return render(request, template, context)