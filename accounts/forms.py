from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms.widgets import NumberInput
# import datetime
from .import models



class DateInput(forms.DateInput):
    input_type = "date"


class AccountsForm(forms.ModelForm):

    class Meta:
        model = models.Accounts
        fields = '__all__'


class SubAccountsForm(forms.ModelForm):

    class Meta:
        model = models.Sub_Accounts
        fields = ('sub_code','sub_description','tag',)


class General_LedgerForm(forms.Form):

    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label='Date')
    description= forms.CharField(label='Description')
    debt_amount = forms.DecimalField(max_digits=10, decimal_places=2,label='Amount')
    credit_amount = forms.DecimalField(max_digits=10, decimal_places=2,label='Amount')


class PvForm(forms.ModelForm):
    ob = [4000,4120,4500,4700,4900,5000,5200,3020,4950,5100,5940,4600,5960,1000,11000]
    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    sub_account = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__code__in=ob).order_by('sub_description'))

    class Meta:
        model = models.Payment_Vouchers
        fields = ('transaction_date','sub_account','company','description')

class Pv_detailsForm(forms.ModelForm):
    description = forms.CharField(label=False)
    amount = forms.CharField(label=False)
    class Meta:
        model = models.APv_details
        fields = ('description','amount',)


class paymentform(forms.Form):
    ob = [1103,1200]
    amount_paid = forms.DecimalField(decimal_places=2,label='Amount')


class Student_Bill_Detail_Form(forms.ModelForm):
    description = forms.CharField(label=False)
    amount = forms.CharField(label=False)
    class Meta:
        model = models.Student_Bill_Details
        fields = ('description','amount',)


class transferform(forms.ModelForm):
    ob = [1103,1200,2154]
    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    fromaccount_code = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__code__in=ob).order_by('sub_description'), label='From')
    toaccount_code = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__code__in=ob).order_by('sub_description'), label='To')
    tran_dec = forms.CharField(label='Transfer Description')

    class Meta:
        model = models.Transfers
        fields = ('transaction_date','fromaccount_code','tran_dec','toaccount_code','amount')

class Assetsform(forms.ModelForm):

    assets = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__code=1000).order_by('sub_description'), label='Assets')

    class Meta:
        model = models.FixedAssets
        fields = ('assets','value','depreciation_rate')

class Discountform(forms.Form):

    discount = forms.DecimalField(decimal_places=2,label='Discount (%)')

    def clean(self, *args, **kwargs):
        discount = self.cleaned_data.get('discount')
        if discount:

            if discount <= 0:
                raise forms.ValidationError(
                    {'discount': ["Discount cannot be less than or equal to 0 "]})
            elif discount > 15:
                raise forms.ValidationError(
                    {'discount': ["Discount cannot be greater than 15% "]})

        return super(Discountform, self).clean(*args, **kwargs)
