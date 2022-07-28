from __future__ import print_function
import threading
from django.http import request
from school_management_system.settings import endPoint,apiKey,mulan_sender_id
from twilio.rest import Client
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .models import *
from telesign.messaging import MessagingClient
import requests
from .models import Parents,Students



class  NotificationThreads(threading.Thread):
    def __init__(self,newsms,sms,students):
        self.newsms = newsms
        self.sms = sms
        self.students = students
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        item =[]
        
        item.append(self.sms.venue)
        if self.sms.event_date:
            item.append(self.sms.event_date)
        if self.sms.event_time:
            item.append(self.sms.event_time)
        if self.sms.phone:
            item.append(self.sms.phone)

       
        for i in self.students:
            print(i.id)
            
            try:
                body = [
                    'Dear '+i.parent_id.father_name,
                    '\n'+ self.newsms,
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
                Sms_errormesseage.objects.create(message=self.newsms,venue=self.sms.venue,event_time=self.sms.event_time,event_date=self.sms.event_date,recepient=i.parent_id.father_phone)
            
            try:
                body = [
                    'Dear '+i.parent_id.mother_name,
                    '\n'+ self.newsms,
                    
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
                Sms_errormesseage.objects.create(message=self.newsms,venue=self.sms.venue,event_time=self.sms.event_time,event_date=self.sms.event_date,recepient=i.parent_id.father_phone)

    

