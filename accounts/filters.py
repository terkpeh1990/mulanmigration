import django_filters
from django import forms
from django_filters import DateFilter, CharFilter, NumberFilter
from .models import *



class DateInput(forms.DateInput):
    input_type = 'date'


class GeneralLedgerFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="transaction_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="transaction_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = General_Ledger
        fields = ['start_date','end_date', 'sub_code']

class PayablesFilter(django_filters.FilterSet):
    pv_no = CharFilter(field_name='reference',
                            lookup_expr='exact', label='Pv No.')


    start_date = DateFilter(field_name="transaction_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="transaction_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Account_Payables
        fields = ['start_date','end_date', 'sub_code','pv_no']


class ReceivableFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="transaction_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="transaction_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Account_Receivable
        fields = ['start_date','end_date']


class TransferFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="transaction_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="transaction_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Transfers
        fields = ['start_date','end_date']



class ARevenueFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="created_date", lookup_expr='gte', label='Income Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="created_date", lookup_expr='lte', label='Income End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = ARevenue
        fields = ['start_date', 'end_date', 'id',
                  'account_code', 'amount', 'created_date', 'company']