from django.http import response
from django.shortcuts import render
from rest_framework.serializers import Serializer
from school.models import Students
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import datetime
from accounts.models import Account_Receivable, General_Ledger, Sub_Accounts,Bank_Cash_Ledger,ARevenue,School_Bank_payments,fees_transaction #new
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from school.models import Students
# from .thread import BankThread
from .tasks import send_notification_alert
from .import tasks
import sys
from django.core import serializers





class student(generics.ListAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields =['^id','^Surname','^firstname']
    ordering_fields = ['id','Surname','firstname']
    ordering = ['-id']


class payment(generics.CreateAPIView):

    serializer_class = PaymentSerializer




    def create(self, request, *args, **kwargs,):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            cc=serializer.save()
            ar =Account_Receivable.objects.get(student_id=cc.student_id)
            ar.amount -= cc.amount
            ar.save()
            cc.balance = ar.amount
            cc.save()
            student = Students.objects.get(id=cc.student_id)
            bb=fees_transaction.objects.create(amount=cc.amount,balance=cc.balance,student_id=cc.student_id)
            sub_code = Sub_Accounts.objects.get(sub_code=1110)
            today = datetime.datetime.now()
            General_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description='Payment of School Fees' ,debit=cc.amount)
            Bank_Cash_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description='Payment of School Fees',amount=cc.amount)
            # # bb =PaymentSucessSerializer(vv)
            # bb=serializers.serialize("json", vv
            # )
            print
            # content_type="application/json"
            # send_notification_alert.delay(
            #         amount=bb.amount,
            #         student=bb.student_id,
            #         balance=bb.balance
            #     )

        return super(payment, self).create(request, *args, **kwargs)
