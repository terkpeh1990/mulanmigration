from django import forms
from django.forms import Form
from django.contrib.auth import authenticate, get_user_model
import datetime
from .import models
from .models import SalonCategory, SalonProduct, SalonInventory_records,  SalonInventory, SalonOrder_Details


class DateInput(forms.DateInput):
    input_type = "date"


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.SalonCategory
        fields = ('name', )

        labels = {
            'name': 'Name',
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = models.SalonProduct
        fields = ('name', 'category', 'unit_price',)


class RestockForm(forms.ModelForm):
    # catname = SalonCategory.objects.get(name='Products')
    product = forms.ModelChoiceField(
        queryset=SalonProduct.objects.filter(category = 1).order_by('name'))

    class Meta:
        model = models.SalonInventory_records
        fields = ('product', 'quantity',)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.SalonCustomer
        fields = ('name', 'phone',)



class OrderdetailsForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=SalonProduct.objects.order_by('name'))

    def clean(self, *args, **kwargs):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')

        if product.category.name == 'Products':
            try:
                check = SalonInventory.objects.get(product_id=product)
                if check.avialable_stock < quantity:
                    raise forms.ValidationError(
                        {'quantity': ["Quantity cannot be more than the avialable stock"]})
            except SalonInventory.DoesNotExist:
                pass
        return super(OrderdetailsForm, self).clean(*args, **kwargs)

    class Meta:
        model = models.SalonOrder_Details
        fields = ('product', 'quantity',)

        labels = {
            'quantity': 'Qty',


        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.SalonOrder
        fields = ('amount_paid',)

class InventoryForm(forms.Form):
    quantity = forms.CharField(max_length=30)


