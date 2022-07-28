from django.contrib import admin
from .models import *
from .models import Profile

# Register your models here.
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('name')

# #     # search_fields = ('name',)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_code','amount','stubill','company')
    list_filter = ('account_code', 'company')
    search_fields = ['id','amount']
    ordering = ['-id']

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'Surname','middlename','firstname','dob','course_id','parent_id')
    list_filter = ('course_id',)
    search_fields = ['id','course_id__class_name','parent_id__father_name','parent_id__mother_name','Surname','firstname']
    ordering = ['-id']

class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'Surname','middlename','firstname','dob','course_id','phone')
    list_filter = ('course_id',)
    search_fields = ['id','course_id__class_name','Surname','firstname','phone']
    ordering = ['-id']

class ParentAdmin(admin.ModelAdmin):
    list_display = ('id', 'father_name','father_phone','frelationship','mother_name','mother_phone','mrelationship')
    search_fields = ['id','father_name','mother_name']
    ordering = ['-id']


class BilingAdmin(admin.ModelAdmin):
    list_display = ('id','student_id', 'session_year_id','term_year_id','billing_type','total','amount_paid')
    search_fields = ['id','student_id__id','billing_type__name','student_id__firstname','student_id__Surname']
    ordering = ['-id']

class Payment_HistoryAdmin(admin.ModelAdmin):
    list_display = ('id','billing_id', 'amount_paid')
    search_fields = ['id','billing_id__id','amount_paid',]
    ordering = ['-id']

class Payment_HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount_paid','billing_id')
    search_fields = ['id','amount_paid']
    ordering = ['-id']


class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_id','student_id','acadamic_years')
    list_filter = ('acadamic_years', 'student_id','class_id')
    search_fields = ['id','class_id','student_id']
    ordering = ['-id']

class StaffClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_id','staff_id','acadamic_year')
    list_filter = ('acadamic_year', 'staff_id','class_id')
    search_fields = ['id','class_id','staff_id','acadamic_year']
    ordering = ['-id']

admin.site.register(Staffs,StaffAdmin)
admin.site.register(Profile)
admin.site.register(Parents,ParentAdmin)
admin.site.register(Attendance)
admin.site.register(Bills)
admin.site.register(Bills_class)
admin.site.register(StudentBill)
admin.site.register(Pv)
admin.site.register(Pv_details)
admin.site.register(Revenue,RevenueAdmin)
admin.site.register(Expenditure)
admin.site.register(Payroll)
admin.site.register(Company_group)
admin.site.register(Bulksend)
admin.site.register(SMS)
admin.site.register(Group_sms)
admin.site.register(Account_code)
admin.site.register(DailyClassReport)
admin.site.register(Students,StudentAdmin)
admin.site.register(Billing,BilingAdmin)
admin.site.register(Payment_History,Payment_HistoryAdmin)
admin.site.register(Grouping_name)
admin.site.register(Terms)
admin.site.register(Students_Class,StudentClassAdmin)
admin.site.register(Staff_Class,StaffClassAdmin)
admin.site.register(SessionYearModel)
admin.site.register(Subjects)
admin.site.register(SchClass)
admin.site.register(HostOrder)
# admin.site.register(HostOrder_Detail)
