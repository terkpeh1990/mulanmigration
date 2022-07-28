import django_filters
from django import forms
from django_filters import DateFilter, CharFilter, NumberFilter
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class AccountRecievableFilter(django_filters.FilterSet):
    # customer = CharFilter(field_name='customer',
    #                       lookup_expr='icontains', label='Customer')
    start_date = DateFilter(field_name="order_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="order_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Order
        fields = [ 'start_date', 'end_date', 'customer', 'order_date']

class ReportFilter(django_filters.FilterSet):
    
    start_date = DateFilter(field_name="order_id__order_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="order_id__order_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Order_Details
        fields = [ 'start_date', 'end_date', ]

