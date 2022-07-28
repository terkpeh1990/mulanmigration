from django.contrib.auth.models import AbstractUser, User
from django_resized import ResizedImageField
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.sessions.models import Session
import datetime
from school.utils import incrementor
from crum import get_current_user
from simple_history.models import HistoricalRecords

User = settings.AUTH_USER_MODEL


# Create your models here.
class SalonCategory(models.Model):
    name = models.CharField(max_length=50)
    # created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL,related_name='SCcreatedby' ,blank=True, null=True,default=None)
    # modified = models.DateTimeField(auto_now=True)
    # modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='SCdmodifiedby', blank=True, null=True, default=None)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     user = get_current_user()
    #     if user and not user.pk:
    #         user = None
    #     if not self.pk:
    #         self.created_by = user
    #     self.modified_by = user
    #     super(SalonCategory, self).save(*args, **kwargs)


class SalonProduct(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(SalonCategory, on_delete=models.CASCADE)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    # created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL,related_name='SPcreatedby' ,blank=True, null=True,default=None)
    # modified = models.DateTimeField(auto_now=True)
    # modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='SPmodifiedby', blank=True, null=True, default=None)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


    def save(self):
        # user = get_current_user()
        # if user and not user.pk:
        #     user = None
        if not self.id:
            number = incrementor()
            self.id = "PR" + str(number())
            while SalonProduct.objects.filter(id=self.id).exists():
                self.id = "PR" + str(number())
        #     self.created_by = user
        # self.modified_by = user
        super(SalonProduct, self).save()


class SalonInventory(models.Model):
    product_id = models.ForeignKey(SalonProduct, on_delete=models.CASCADE)
    instock = models.PositiveIntegerField(default=0)
    outgoing = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    avialable_stock = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    # created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL,related_name='SIcreatedby' ,blank=True, null=True,default=None)
    # modified = models.DateTimeField(auto_now=True)
    # modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='SImodifiedby', blank=True, null=True, default=None)


    history = HistoricalRecords()

    def __str__(self):
        return self.product_id.name + " " + str(self.avialable_stock)

    def save(self, *args, **kwargs):
        self.avialable_stock = self.instock - self.outgoing
        self.avialable_stock_cost = self.avialable_stock * self.unit_price
        # user = get_current_user()
        # if user and not user.pk:
        #     user = None
        # if not self.pk:
        #     self.created_by = user
        # self.modified_by = user
        super(SalonInventory, self).save(*args, **kwargs)


class SalonClosing_stocks(models.Model):
    ac = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    product = models.ForeignKey(SalonProduct, on_delete=models.CASCADE)
    closing_stock = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    close_status = models.CharField(
        max_length=10, choices=ac, null=True, blank=True)
    closing_stock_date = models.DateField(auto_now_add=True)

    # created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='SCScreatedby', blank=True, null=True,
    #                               default=None)
    # modified = models.DateTimeField(auto_now=True)
    # modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='SCSmodefiedby', blank=True, null=True,
    #                                 default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name + " " + str(self.closing_stock)

    # def save(self, *args, **kwargs):
    #     user = get_current_user()
    #     if user and not user.pk:
    #         user = None
    #     if not self.pk:
    #         self.created_by = user
    #     self.modified_by = user
    #     super(SalonClosing_stocks, self).save(*args, **kwargs)




class SalonInventory_records(models.Model):
    stat = (
        ('Incoming', 'Incoming'),
        ('Outgoing', 'Outgoing'),
    )

    accept = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )

    transaction_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(SalonProduct, on_delete=models.CASCADE)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=10, choices=stat, null=True, blank=True)
    approval = models.CharField(
        max_length=10, choices=accept, null=True, blank=True)

    # created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='SCScreatedby', blank=True, null=True,
    #                               default=None)
    # modified = models.DateTimeField(auto_now=True)
    # modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='SCSmodefiedby', blank=True, null=True,
    #                                 default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.avialable_stock_cost = self.quantity * self.unit_price
        # user = get_current_user()
        # if user and not user.pk:
        #     user = None
        # if not self.pk:
        #     self.created_by = user
        # self.modified_by = user
        super(SalonInventory_records, self).save(*args, **kwargs)


class SalonCustomer(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    due_dates = models.DateField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.id:
            number = incrementor()
            self.id = "CUS" + str(number())
            while SalonCustomer.objects.filter(id=self.id).exists():
                self.id = "CUS" + str(number())
        super(SalonCustomer, self).save(*args, **kwargs)





class SalonOrder(models.Model):
    pay = (
        ('Part Payment', 'Part Payment'),
        ('Full Payment', 'Full Paument'),
        ('No Payment', 'No Payment'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    order_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(
        SalonCustomer, on_delete=models.DO_NOTHING, null=True, blank=True)
    gross_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    payments = models.CharField(
        max_length=25, choices=pay, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    money_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    money_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)


    history = HistoricalRecords()

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        self.total_price = float(self.gross_price)
        cc = self.total_price - float(self.amount_paid)
        if cc < 0.00:
            self.balance = 0.00
        else:
            self.balance =cc
        self.money_balance = float(self.amount_paid) - float(self.total_price)

        if self.total_price == self.amount_paid:
            self.payments = 'Full Payment'
        elif self.amount_paid > 0 and self.amount_paid < self.total_price:
            self.payments = 'Part Payment'
        else:
            self.payments = 'No Payment'

        # user = get_current_user()
        # if user and not user.pk:
        #     user = None
        if not self.id:
            number = incrementor()
            self.id = "IGS" + str(number())
            while SalonOrder.objects.filter(id=self.id).exists():
                self.id = "IGS" + str(number())
        #     self.created_by = user
        # self.modified_by = user
        super(SalonOrder, self).save(*args, **kwargs)


class SalonOrder_Details(models.Model):
    product = models.ForeignKey(SalonProduct, on_delete=models.DO_NOTHING)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField()
    gross_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    order_id = models.ForeignKey(SalonOrder, on_delete=models.DO_NOTHING)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.gross_price = self.unit_price * self.quantity
        super(SalonOrder_Details, self).save(*args, **kwargs)


