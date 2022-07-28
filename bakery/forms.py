from django import forms
from django.forms import Form
from django.contrib.auth import authenticate, get_user_model
import datetime
from .import models
from .models import Category, Product, Inventory_records, Damages, Inventory


class DateInput(forms.DateInput):
    input_type = "date"

class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ('name', )

        labels = {
            'name': 'Name',
        }

class ProductForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ('name','category','unit_price','jumia_unit_price',)


class RestockForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by('name'))

    class Meta:
        model = models.Inventory_records
        fields = ('product', 'quantity',)


class DamageForm(forms.ModelForm):
    product_id = forms.ModelChoiceField(
        queryset=Product.objects.order_by('name'))
    class Meta:
        model = models.Damages
        fields = ('product_id', 'quantity','cause')
        labels = {
            'cause': 'Cause of Damage',
        }

    def clean(self, *args, **kwargs):
        product = self.cleaned_data.get('product_id')
        quantity = self.cleaned_data.get('quantity')
        if product:
            try:
                check = Inventory.objects.get(product_id=product)
                if check.avialable_stock < quantity:
                    raise forms.ValidationError({'quantity': ["Damages cannot be more than the avialable stock"]})
            except Inventory.DoesNotExist:
                pass
        return super(DamageForm,self).clean(*args, **kwargs)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('name', 'phone', 'due_dates')
        widgets = {
            'due_dates': DateInput(),
        }


class OrderdetailsForm(forms.ModelForm):

    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by('name'),label=False)
    quantity = forms.IntegerField(label=False)
    def clean(self, *args, **kwargs):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')
        if product:
            try:
                check = Inventory.objects.get(product_id=product)
                if check.avialable_stock < quantity:
                    raise forms.ValidationError(
                        {'quantity': ["Quantity cannot be more than the avialable stock"]})
            except Inventory.DoesNotExist:
                pass

        return super(OrderdetailsForm, self).clean(*args, **kwargs)
    class Meta:
        model = models.Order_Details
        fields = ('product', 'quantity',)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ('amount_paid',)

class paymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class TakeOrderdetailsForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by('name'),label=False)
    quantity = forms.IntegerField(label=False)
    class Meta:
        model = models.Order_Details
        fields = ('product', 'quantity',)


class InventoryForm(forms.Form):
    quantity = forms.CharField(max_length=30)

class SnackForm(forms.ModelForm):
    class Meta:
        model = models.Snacks
        fields = ('activity',)

class SnackDetailForm(forms.ModelForm):
    class Meta:
        model = models.Snack_detail
        fields = ('student_name','snack')

