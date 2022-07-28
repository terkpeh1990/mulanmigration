import django_filters
from django import forms
from django_filters import DateFilter, CharFilter, NumberFilter,ModelChoiceFilter
from .models import *
from accounts.models import ARevenue


class DateInput(forms.DateInput):
    input_type = 'date'


class StudentBillFilter(django_filters.FilterSet):
    student_id = CharFilter(field_name='student_id',
                            lookup_expr='exact', label='Student ID')

    class Meta:
        model = StudentBill
        fields = ['id', 'student_id', 'session_year_id', 'term_year_id', 'bill_id',
                  'amount', 'amount_paid', 'balance', 'paidby', 'paidbyphone']




class AccountRecievableFilter(django_filters.FilterSet):
    student_id = CharFilter(field_name='student_id',
                            lookup_expr='exact', label='Student ID')
    start_date = DateFilter(field_name="bill_date", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="bill_date", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = StudentBill
        fields = ['id','start_date','end_date', 'student_id', 'session_year_id', 'term_year_id', 'bill_id',
                  'amount', 'amount_paid', 'balance', 'paidby', 'paidbyphone', 'bill_date']

class RevenueFilter(django_filters.FilterSet):

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


class ExpenditureFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="created_date", lookup_expr='gte', label='Expenditure Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="created_date", lookup_expr='lte', label='Expenditure End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )

    class Meta:
        model = Expenditure
        fields = ['start_date', 'end_date', 'id',
                  'account_code', 'amount', 'created_date', 'company']


class StaffFilter(django_filters.FilterSet):
    id = CharFilter(field_name='id',
                            lookup_expr='exact', label='Staff ID')
    firstname = CharFilter(field_name='firstname',
                            lookup_expr='exact', label='First Name')

    surname = CharFilter(field_name='Surname',
                            lookup_expr='exact', label='Surname')

    class Meta:
        model = Staffs
        fields = [ 'id','branch','firstname', 'Surname','branch' ]


class AttendanceFilter(django_filters.FilterSet):


    start_date = DateFilter(field_name="created_at", lookup_expr='gte', label='Start Date',
                            widget=DateInput(
                                attrs={
                                    'class': 'datepicker'
                                }
                            )

                            )

    end_date = DateFilter(field_name="created_at", lookup_expr='lte', label='End Date',
                          widget=DateInput(
                              attrs={
                                  'class': 'datepicker'
                              }
                          )

                          )
    classes = ModelChoiceFilter(field_name="attendance_id__class_id", queryset=SchClass.objects.all(),label='Class')
    term = ModelChoiceFilter(field_name="attendance_id__term_year_id", queryset=SessionTerm.objects.all().order_by('-id'),label='Term')

    class Meta:
        model = AttendanceReport
        fields = ['start_date','end_date', 'student_id','classes','term'
                  ]

    class Meta:
        model = AttendanceReport
        fields = ['start_date','end_date', 'student_id','classes'
                  ]


class StaffAttendanceFilter(django_filters.FilterSet):

    classes = ModelChoiceFilter(field_name="attendance_id__class_id", queryset=SchClass.objects.all(),label='Class')
    term = ModelChoiceFilter(field_name="attendance_id__term_year_id", queryset=SessionTerm.objects.all().order_by('-id'),label='Term')

    class Meta:
        model = AttendanceReport
        fields = ['student_id','classes','term'
                  ]