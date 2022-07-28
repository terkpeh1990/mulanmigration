from django.contrib.auth.models import AbstractUser, User
from django.db import models
from crum import get_current_user
from django.db.models import Count
from django.conf import settings
from django.contrib.sessions.models import Session
from simple_history.models import HistoricalRecords
from school.utils import incrementor
from school.models import Company_group
import datetime
from bakery.models import Order,UserShift
from partytree.models import Orders
from school.models import Students, SessionYearModel, SessionTerm
from school.utils import billincrementor
from bankapi import tasks
from rest_framework.response import Response

from school_management_system.settings import endPoint,apiKey,mulan_sender_id
import requests
import sys


User = settings.AUTH_USER_MODEL


# Create your models here.

class Accounts(models.Model):
    code = models.CharField(max_length=300)
    description = models.CharField(max_length=300)

    history = HistoricalRecords()


    def __str__(self):
        return  str(self.code)

class Sub_Accounts(models.Model):
    sts= (
        ('Mulan','Mulan'),
        ('Partytree','Partytree'),
        ('Mulan Construct','Mulan Construct'),

    )
    code = models.ForeignKey(Accounts, on_delete= models.CASCADE)
    sub_code = models.CharField(max_length=300)
    sub_description = models.CharField(max_length=300)
    tag = models.CharField(max_length=20, choices= sts, default='Mulan')


    history = HistoricalRecords()


    def __str__(self):
        return  str(self.sub_code) + '----' + self.sub_description


class General_Ledger(models.Model):
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cedit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='glcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='glmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(General_Ledger, self).save(*args, **kwargs)

class Payment_Vouchers(models.Model):
    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('cancelled','cancelled'),
        ('void','void'),
    )
    id = models.CharField(max_length=100, primary_key=True)
    sub_account = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    company = models.ForeignKey(Company_group, on_delete=models.CASCADE,  blank=True, null=True)
    description = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices= sts)
    created_date = models.DateField(auto_now_add=True)
    transaction_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.description


    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = str(number())
            while Payment_Vouchers.objects.filter(id=self.id).exists():
                self.id = str(number())
        super(Payment_Vouchers, self).save(*args, **kwargs)


class APv_details(models.Model):
    id = models.AutoField(primary_key=True)
    payment_voucher = models.ForeignKey(Payment_Vouchers, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Account_Payables(models.Model):
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference = models.ForeignKey(Payment_Vouchers,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='apcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='apmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Account_Payables, self).save(*args, **kwargs)


class Pv_Payment_History(models.Model):
    transaction_date = models.DateField(auto_now_add=True)
    reference = models.ForeignKey(Payment_Vouchers,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='hiscreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='hismodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Pv_Payment_History, self).save(*args, **kwargs)





class Bank_Cash_Ledger(models.Model):
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # reference = models.CharField(max_length=300,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='tcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='tmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Bank_Cash_Ledger, self).save(*args, **kwargs)


class AExpenditure(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    account_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_date = models.DateField(auto_now_add=True)
    pvno = models.ForeignKey(Payment_Vouchers, on_delete=models.CASCADE ,blank=True, null=True)
    company = models.ForeignKey(
        Company_group, on_delete=models.CASCADE,related_name='ecompany',  blank=True, null=True)

    def __str__(self):
        return self.account_code + " " + str(self.amount)

    def save(self, *args, **kwargs):


        if not self.id:
            number = incrementor()
            self.id = number()
            while AExpenditure.objects.filter(id=self.id).exists():
                self.id = number()
        super(AExpenditure, self).save(*args, **kwargs)

class ARevenue(models.Model):
    sts= (
        ('Cash','Cash'),
        ('Momo','Momo'),
        ('Jumia','Jumia'),

    )
    stss= (
        ('New','New'),
        ('Old','Old'),

    )
    id = models.CharField(max_length=100, primary_key=True)
    account_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    shift = models.ForeignKey(UserShift, on_delete=models.CASCADE,blank=True, null=True)#new
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices= sts,default='Cash')
    close = models.CharField(max_length=10, choices= stss,default='Old')
    created_date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(
        Company_group, on_delete=models.CASCADE,related_name='icompany',  blank=True, null=True)

    def __str__(self):
        return str(self.account_code) + " " + str(self.amount)

    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = number()
            while ARevenue.objects.filter(id=self.id).exists():
                self.id = number()
        super(ARevenue, self).save(*args, **kwargs)


class Student_Bill(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    student_id = models.ForeignKey(
        Students, on_delete=models.DO_NOTHING, null=True, blank=True)
    session_year_id = models.ForeignKey(
        SessionYearModel, on_delete=models.CASCADE, null=True, blank=True)
    term_year_id = models.ForeignKey(SessionTerm, on_delete=models.CASCADE,null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bill_date  = models.DateField(auto_now_add=True)
    parent_id = models.CharField(max_length=255, null=True, blank=True)
    bill_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.id:
            number = billincrementor()
            self.id = number()
            while Student_Bill.objects.filter(id=self.id).exists():
                self.id = number()
        super(Student_Bill, self).save(*args, **kwargs)

class Student_Bill_Details(models.Model):
    bill_id = models.ForeignKey(
        Student_Bill, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Account_Receivable(models.Model):
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # student_bill_ref = models.ForeignKey(Student_Bill, on_delete=models.CASCADE,null=True,blank=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE,null=True,blank=True)
    bakes_order_no = models.ForeignKey(Order, on_delete=models.CASCADE,null=True,blank=True)
    partytree_order_no = models.ForeignKey(Orders, on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='arcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='armodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Account_Receivable, self).save(*args, **kwargs)


class School_Bank_payments(models.Model):
    transaction_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    student_id = models.CharField(max_length=255)



    history = HistoricalRecords()

    def __str__(self):
        return self.description + " "+ self.amount

    # def save(self, *args, **kwargs):



    #     super(School_Bank_payments, self).save(*args, **kwargs)

class fees_transaction(models.Model):
    transaction_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    student_id = models.CharField(max_length=255)

    history = HistoricalRecords()

    def __str__(self):
        return self.description + " "+ self.amount

    # def save(self, *args, **kwargs):
    #     student = Students.objects.get(id=self.student_id)
    #     father_name = student.parent_id.father_name
    #     father_no = student.parent_id.father_phone

    #     mother_name = student.parent_id.mother_name
    #     mother_no = student.parent_id.mother_phone
    #     try:
    #         message = "Dear Parent"  + ",\n\nPayment Notification Details:"+ "\n\nDate : " + str(self.transaction_date) +"\nAmount Paid : "+ "GHC" +" " + str(self.amount) + "\nStudent Name : "+student.Surname + " "+ student.firstname+"\nOutsanding Fees : ""GHC" +" " +str(self.balance)+"\n\nThank you for choosing Mulan Smart Educational Center"
    #         sender_id= mulan_sender_id
    #         url = endPoint + '?key=' + apiKey
    #         response = requests.post(url+'&to='+father_no +'&msg='+message+'&sender_id='+sender_id)

    #         data = response.json()

    #         print(data)
    #     except:
    #         print(sys.exc_info()[0])
    #         return False
    #     try:
    #         message = "Dear Parent"  + ",\n\nPayment Notification Details:"+ "\n\nDate : "+ str(self.transaction_date) +"\nAmount Paid : "+ "GHC" +" " + str(self.amount) + "\nStudent Name : "+student.Surname + " "+ student.firstname+"\nOutsanding Fees : "+"GHC" +" " +str(self.balance)+"\n\nThank you for choosing Mulan Smart Educational Center"
    #         sender_id= mulan_sender_id
    #         url = endPoint + '?key=' + apiKey
    #         response = requests.post(url+'&to='+mother_no +'&msg='+message+'&sender_id='+sender_id)

    #         data = response.json()

    #         print(data)
    #     except IOError:
    #         print(sys.exc_info()[0])
    #         return False

    #     super(fees_transaction, self).save(*args, **kwargs)




class Transfers(models.Model):
    sts= (
        ('Pending','Pending'),
        ('Comfirmed','Comfirmed'),
        ('Cancelled','Cancelled'),

    )
    id = models.CharField(max_length=100, primary_key=True)
    transaction_date = models.DateField()

    tran_dec = models.CharField(max_length=300,default ='Transfer' ,blank=True,null=True)
    status = models.CharField(max_length=10, choices= sts,default='Comfirmed')
    fromaccount_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE, related_name='froms')
    toaccount_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE, related_name='to')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # toamount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='Trcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='trmodifiedby', blank=True, null=True,default=None)


    def __str__(self):
        return self.tran_dec + " " + str(self.amount)

    def save(self, *args, **kwargs):

        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        if not self.id:
            number = incrementor()
            self.id = number()
            while Transfers.objects.filter(id=self.id).exists():
                self.id = number()
        super(Transfers, self).save(*args, **kwargs)



class FixedAssets(models.Model):
    transaction_date = models.DateField(auto_now_add=True)
    assets = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    history = HistoricalRecords()

    def __str__(self):
        return self.assets.sub_description

class Fixed_Assets_Depreciation(models.Model):
    transaction_date = models.DateField(auto_now_add=True)
    assets = models.ForeignKey(FixedAssets, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    depreciated_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    history = HistoricalRecords()

    def __str__(self):
        return self.assets.assets.sub_description


class Discounts(models.Model):

    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.discount_value)

