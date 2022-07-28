import threading
from django.http import request
from school_management_system.settings import TWILIO_ACCOUNT_SID2, TWILIO_AUTH_TOKEN2, TWILIO_PHONE_NUMBER2
from twilio.rest import Client
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .models import *


class  CheckoutThread(threading.Thread):
    def __init__(self, order):
        self.order = order
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        client = Client(TWILIO_ACCOUNT_SID2, TWILIO_ACCOUNT_SID2)
        if self.order.due_date:
            try:
                message = client.messages.create(
                    to="+233" + self.order.customer.phone,
                    from_=TWILIO_PHONE_NUMBER2,
                    body="Dear" + " " + self.order.customer.name + "," + " " + "The total cost of your order with ID" + " "+self.order.id + " " + "is " + " " + "GHC" + " " + str(self.order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(self.order.amount_paid) + " " + " Your order will be ready for delivery or pickup on "+" " + str(self.order.due_date) + " " + ".Thank you for choosing Party Tree Bakes, For all your enquiries and orders, Please contact us on 0302986501 or 0209684708(Whatsapp).")
            except IOError:
                print('fail')
                pass
        else:
            try:
                message = client.messages.create(
                    to="+233" + self.order.customer.phone,
                    from_=TWILIO_PHONE_NUMBER2,
                    body="Dear" + " " + self.order.customer.name + "," + " " + "The total cost of your order with ID" + " "+self.order.id + " " + "is " + " " + "GHC" + " " + str(self.order.total_price) + "." + "  " + " You have made payment of GHC" + " " + str(self.order.amount_paid) + " "  + ".Thank you for choosing Party Tree Bakes, For enquiries and orders, Please contact us on 0302986501 or 0209684708(Whatsapp).")
            except IOError:
                print('fail')
                pass


class  PaymentThread(threading.Thread):
    def __init__(self, order):
        self.order = order
        threading.Thread.__init__(self)

    def run(self):
        print('started')
        client = Client(TWILIO_ACCOUNT_SID2, TWILIO_ACCOUNT_SID2)

        try:
            message = client.messages.create(
                to="+233" + self.order.customer.phone,
                from_=TWILIO_PHONE_NUMBER2,
                body="Dear" + " " + self.order.customer.name + "," + " " + "The total cost of your order with ID" + " "+self.order.id + " " + "is " + " " + "GHC" + " " + str(self.order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(self.order.amount_paid) + " " + ".Thank you for choosing Party Tree Bakes, For enquiries and orders, Please contact us on 0302986501 or 0209684708(Whatsapp).")
        except IOError:
            print('fail')
            pass

