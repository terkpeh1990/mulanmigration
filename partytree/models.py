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

User = settings.AUTH_USER_MODEL


# Create your models here.
class Categorys(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=2000,null=True, blank=True)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    images = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):

    #     if not self.id:
    #         number = incrementor()
    #         self.id = number()
    #         while Products.objects.filter(id=self.id).exists():
    #             self.id = number()
    #     super(Products, self).save(*args, **kwargs)


class Inventorys(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    instock = models.PositiveIntegerField(default=0)
    outgoing = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    avialable_stock = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product_id.name + " " + str(self.avialable_stock)

    def save(self, *args, **kwargs):
        self.avialable_stock = self.instock - self.outgoing
        self.avialable_stock_cost = self.avialable_stock * self.unit_price
        super(Inventorys, self).save(*args, **kwargs)


class Damagess(models.Model):
    acc = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )
    damage_date = models.DateTimeField(auto_now_add=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cause = models.CharField(max_length=255)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    dastatus = models.CharField(
        max_length=10, choices=acc, null=True, blank=True)
    clear = models.BooleanField(default = False)
    # created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL,related_name='dcreatedbys' ,blank=True, null=True,default=None)
    # modified = models.DateTimeField(auto_now=True)
    # modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='dmodifiedbys', blank=True, null=True, default=None)
    # history = HistoricalRecords()

    def __str__(self):
        return self.product_id.name + " " + str(self.quantity)

    def save(self, *args, **kwargs):
        # user = get_current_user()
        self.cost = self.product_id.unit_price * self.quantity
        # if user and not user.pk:
        #     user = None
        # if not self.pk:
        #     self.created_by = user
        # self.modified_by = user
        super(Damagess, self).save(*args, **kwargs)


class Closing_stockss(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    closing_stock = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    closing_stock_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name + " " + str(self.avialable_stock)


class Inventory_recordss(models.Model):
    stat = (
        ('Incoming', 'Incoming'),
        ('Outgoing', 'Outgoing'),
    )

    transaction_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=10, choices=stat, null=True, blank=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.avialable_stock_cost = self.quantity * self.unit_price
        super(Inventory_recordss, self).save(*args, **kwargs)


class Customers(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.id:
            number = incrementor()
            self.id = "CUS" + str(number())
            while Customers.objects.filter(id=self.id).exists():
                self.id = "CUS" + str(number())
        super(Customers, self).save(*args, **kwargs)


class Daily_Session(models.Model):
    stat = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )
    session_date = models.DateField()
    status = models.CharField(max_length=10, choices=stat)


class Orders(models.Model):
    pay = (
        ('Part Payment', 'Part Payment'),
        ('Full Payment', 'Full Paument'),
        ('No Payment', 'No Payment'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    order_date = models.DateField(auto_now_add=True,null=True, blank=True)
    gross_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00,null=True, blank=True)
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

    daily_session = models.ForeignKey(
        Daily_Session, on_delete=models.DO_NOTHING, null=True, blank=True)
    money_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    money_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ('-order_date',)

    def __str__(self):
        return self.id



    def save(self, *args, **kwargs):
        if self.gross_price:
            self.total_price = float(self.gross_price)
        else:
            self.total_price = 0.00
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


        if not self.id:
            number = incrementor()
            self.id = number()
            while Orders.objects.filter(id=self.id).exists():
                self.id = number()
        super(Orders, self).save(*args, **kwargs)


class Order_Detailss(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField()
    gross_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.gross_price = self.unit_price * self.quantity
        super(Order_Detailss, self).save(*args, **kwargs)


class Invoice(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.DO_NOTHING)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = "INV" + str(number())
            while Invoice.objects.filter(id=self.id).exists():
                self.id = "INV" + str(number())
        super(Invoice, self).save(*args, **kwargs)


class Closing_Stock_summery(models.Model):

    close_date = models.DateField(auto_now_add=True, unique=True)
    stock = models.PositiveIntegerField(default=0)
    closing_stock_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.stock)

class Opening_Stock_summery(models.Model):

    close_date = models.DateField(auto_now_add=True, unique=True)
    stock = models.PositiveIntegerField(default=0)
    closing_stock_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.stock)