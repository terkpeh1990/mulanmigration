from django import forms
from django.forms import Form
from django.contrib.auth import authenticate, get_user_model
import datetime
from .import models
from .models import Categorys, Products, Inventory_recordss, Damagess, Inventorys


class DateInput(forms.DateInput):
    input_type = "date"


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Categorys
        fields = ('name', )

        labels = {
            'name': 'Name',
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = models.Products
        fields = ('id','name', 'category', 'unit_price',)


class RestockForm(forms.ModelForm):


    class Meta:
        model = models.Inventory_recordss
        fields = ('quantity',)


class DamageForm(forms.ModelForm):

    class Meta:
        model = models.Damagess
        fields = ( 'quantity','cause')

    # def clean(self, *args, **kwargs):

    #     quantity = self.cleaned_data.get('quantity')
    #     if product:
    #         try:
    #             check = Inventorys.objects.get(product_id=product)
    #             if check.avialable_stock < quantity:
    #                 raise forms.ValidationError(
    #                     {'quantity': ["Damages cannot be more than the avialable stock"]})
    #         except Inventorys.DoesNotExist:
    #             pass
    #     return super(DamageForm, self).clean(*args, **kwargs)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customers
        fields = ('name', 'phone')



class OrderdetailsForm(forms.ModelForm):

    quantity = forms.IntegerField(label=False)

    def clean(self, *args, **kwargs):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError(
                {'quantity': ["Quantity cannot be less than 1"]})
        return super(OrderdetailsForm, self).clean(*args, **kwargs)

    class Meta:
        model = models.Order_Detailss
        fields = ('quantity',)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.Orders
        fields = ('amount_paid',)


class TakeOrderdetailsForm(forms.ModelForm):
    class Meta:
        model = models.Order_Detailss
        fields = ('product', 'quantity',)

class InventoryForm(forms.Form):
    quantity = forms.CharField(max_length=30)

class QtyForm(forms.Form):
    quantity = forms.IntegerField()


class UploadFileForm(forms.Form):
    file = forms.FileField(label=False)

class paymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)