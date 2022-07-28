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
class Category(models.Model):
    name = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    jumia_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #new

    history = HistoricalRecords()


    def __str__(self):
        return self.name

    def save(self):

        if not self.id:
            number = incrementor()
            self.id = "PR" + str(number())
            while Product.objects.filter(id=self.id).exists():
                self.id = "PR" + str(number())
        super(Product, self).save()

class Inventory(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    instock = models.PositiveIntegerField(default=0)
    outgoing = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    avialable_stock = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    history = HistoricalRecords()

    def __str__(self):
        return self.product_id.name + " " + str(self.avialable_stock)

    def save(self,*args, **kwargs):
        self.avialable_stock = self.instock - self.outgoing
        self.avialable_stock_cost = self.avialable_stock * self.unit_price
        super(Inventory, self).save(*args, **kwargs)


class Damages(models.Model):
    acc = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )
    damage_date = models.DateTimeField(auto_now_add=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cause = models.CharField(max_length=255)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    dastatus = models.CharField(
        max_length=10, choices=acc, null=True, blank=True)
    clear = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL,related_name='dcreatedby' ,blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='dmodifiedby', blank=True, null=True, default=None)
    history = HistoricalRecords()

    def __str__(self):
        return self.product_id.name + " " + str(self.quantity)

    def save(self, *args, **kwargs):
        user = get_current_user()
        self.cost = self.product_id.unit_price * self.quantity
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Damages, self).save(*args, **kwargs)




class Inventory_records(models.Model):
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=stat, null=True, blank=True)
    approval = models.CharField(max_length=10, choices=accept, null=True, blank=True)
    clear = models.BooleanField(default = False)
    created_by = models.ForeignKey('auth.User', related_name='IRcreatedby', on_delete=models.SET_NULL, blank=True, null=True,
                                   default=None)

    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='IRmodifiedby', blank=True, null=True,
                                    default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.avialable_stock_cost = self.quantity * self.unit_price
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Inventory_records, self).save(*args, **kwargs)



class Customer(models.Model):
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
            while Customer.objects.filter(id=self.id).exists():
                self.id = "CUS" + str(number())
        super(Customer, self).save( *args, **kwargs)

class Daily_Session(models.Model):
    stat =(
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )
    session_date = models.DateField()
    status = models.CharField(max_length=10, choices=stat)

class Shift(models.Model): #new
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class UserShift(models.Model):#new
    stat =(
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )
    profile = models.ForeignKey('school.Profile', on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=10, choices=stat)
    status_checking = models.BooleanField(default=True)

    class Meta():
        ordering = ('-id',)

    def __str__(self):
        return self.status

class Snacks(models.Model):
    sn =(
        ('Snack', 'Snack'),
        ('CEO', 'CEO'),
    )
    sat =(
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    activity= models.CharField(max_length=25, choices=sn)
    status = models.CharField(max_length=25, choices=sat)
    date = models.DateField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = str(number())
            while Snacks.objects.filter(id=self.id).exists():
                self.id = str(number())
        super(Snacks, self).save(*args, **kwargs)

    def __str__(self):
        return self.activity


class Snack_detail(models.Model):
    student_name = models.CharField(max_length=255)
    snack = models.ForeignKey(Snacks, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.student_name

class Order(models.Model):
    pay =(
        ('Part Payment', 'Part Payment'),
        ('Full Payment', 'Full Paument'),
        ('No Payment', 'No Payment'),
    )
    order_type =(
        ('Internal', 'Internal'),
        ('Jumia', 'Jumia'),

    )
    id = models.CharField(max_length=2000, primary_key=True)
    order_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    snack = models.ForeignKey(Snacks, on_delete=models.CASCADE, null=True, blank=True)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price =models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payments= models.CharField(max_length=25, choices=pay, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    clear = models.BooleanField(default = False)
    daily_session = models.ForeignKey(Daily_Session, on_delete= models.DO_NOTHING, null=True, blank=True)
    money_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    money_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    usershift = models.ForeignKey(UserShift, on_delete=models.CASCADE,null=True, blank=True)#new
    ordertype= models.CharField(max_length=25, choices=order_type, null=True, blank=True)#new
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ORcreatedby', blank=True, null=True,
                                   default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ORmodifiedby', blank=True, null=True,
                                    default=None)
    history = HistoricalRecords()

    class Meta:
        ordering = ('-order_date',)


    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if self.gross_price:
                self.total_price = float(self.gross_price)
        else:
            self.gross_price= 0.00
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

        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.id:
            number = incrementor()
            self.id = str(number())
            while Order.objects.filter(id=self.id).exists():
                self.id = str(number())
            self.created_by = user
        self.modified_by = user

        super(Order, self).save( *args, **kwargs)

class Order_Details(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField()
    gross_price =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    history = HistoricalRecords()
    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.gross_price = self.unit_price * self.quantity
        super(Order_Details, self).save( *args, **kwargs)

class Invoice(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    order_id= models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = "INV" + str(number())
            while Invoice.objects.filter(id=self.id).exists():
                self.id = "INV" + str(number())
        super(Invoice, self).save(*args, **kwargs)


class loginrecords(models.Model):
    user = models.CharField(max_length=250)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_principal = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_account = models.BooleanField(default=False)
    is_bank = models.BooleanField(default=False)
    is_bakery = models.BooleanField(default=False)
    is_partytree = models.BooleanField(default=False)
    is_irishgreen = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user


class BClosing_Stock_summery(models.Model):

    close_date = models.DateField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    closing_stock_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    usershift = models.ForeignKey(UserShift, on_delete=models.CASCADE,null=True, blank=True)#new



    def __str__(self):
        return str(self.close_date)

class Closing_stocks(models.Model):
    ac = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    closing_stock = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    close_status = models.CharField(
        max_length=10, choices=ac, null=True, blank=True)
    closing_stock_date = models.DateField(auto_now_add=True)
    stock_summery = models.ForeignKey(BClosing_Stock_summery, on_delete=models.CASCADE,null=True, blank=True)#new
    clear = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ccreatedby', blank=True, null=True,
                                   default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='cmodefiedby', blank=True, null=True,
                                    default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name + " " + str(self.closing_stock)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Closing_stocks, self).save(*args, **kwargs)

class BOpening_Stock_summery(models.Model):

    close_date = models.DateField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    closing_stock_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    usershift = models.ForeignKey(UserShift, on_delete=models.CASCADE,null=True, blank=True)#new



    def __str__(self):
        return str(self.stock)


class Opening_stocks(models.Model):
    ac = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    closing_stock = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    close_status = models.CharField(
        max_length=10, choices=ac, null=True, blank=True)
    closing_stock_date = models.DateField(auto_now_add=True)
    open_stock_summery = models.ForeignKey(BOpening_Stock_summery, on_delete=models.CASCADE,null=True, blank=True)#new
    clear = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ocreatedby', blank=True, null=True,
                                   default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='omodefiedby', blank=True, null=True,
                                    default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name + " " + str(self.closing_stock)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Opening_stocks, self).save(*args, **kwargs)
















