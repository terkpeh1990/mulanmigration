import threading
from django.http import request
from school_management_system.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from twilio.rest import Client
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .models import *





class  ParentsmsThread(threading.Thread):
    def __init__(self, parent):
        self.parent = parent
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_SID)

        try:
            message = client.messages.create(
                    to="+233" + self.parent.father_phone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear" + " " + self.parent.father_name + "," + " " + "Your username is:" + " " + "'" + self.parent.id+"'" + " " + "and password is: 'password@12345'. Please note that you will be asked to change your password on your first login to https://msac.pythonanywhere.com/ .Thank you ---- MULAN SMART SCHOOL MANAGEMENT SYSTEM")
            message = client.messages.create(
                    to="+233" + self.parent.mother_phone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear" + " " + self.parent.mother_name + "," + " " + "Your username is:" + " " + "'" + self.parent.id + "'" + " " + "and password is: 'password@12345'. Please note that you will be asked to change your password on your first login to https://msac.pythonanywhere.com/ . Thank you ---- MULAN SMART SCHOOL MANAGEMENT SYSTEM")
        except IOError:
            print('fail')
            pass


class  studentsmsThread(threading.Thread):
    def __init__(self, student):
        self.student = student
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_SID)

        try:
            message = client.messages.create(
                to="+233" + self.student.parent_id.father_phone,
                from_=TWILIO_PHONE_NUMBER,
                body="Dear" + " " + self.student.parent_id.father_name + "," + " " + "the student id of your child is"+" "+ self.student.id +".Thank you ---- MULAN SMART SCHOOL MANAGEMENT SYSTEM")
            message = client.messages.create(
                to="+233" + self.student.parent_id.mother_phone,
                from_=TWILIO_PHONE_NUMBER,
                body="Dear" + " " + self.student.parent_id.mother_name + "," + " " + "the student id of your child is"+" " + self.student.id + ".Thank you ---- MULAN SMART SCHOOL MANAGEMENT SYSTEM")
        except IOError:
            print('fail')
            pass

