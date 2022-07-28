from unicodedata import name
from django.urls import path
from django.conf import settings

from accounts import receivables


from .import accounts
from .import sub_accounts
from .import general_ledger
from .import pv
from .import payerbles
from .import student_bill
from .import transfers
from .import account_dashboard
from .import fixed_assets



app_name = 'accounts'

urlpatterns = [
    path('manage_accounts',accounts.manage_accounts,name='manage_accounts'),
    path('edit_accounts/<str:pk>/',accounts.edit_accounts,name='edit_accounts'),


    path('sub_accounts/<str:pk>/',sub_accounts.sub_accounts,name='sub_accounts'),
    path('edit_sub_accounts/<str:pk>/',sub_accounts.edit_sub_accounts,name='edit_sub_accounts'),

    path('general_ledger',general_ledger.general_ledger,name='general_ledger'),


    path('general_ledger',general_ledger.general_ledger,name='general_ledger'),
    path('create_pv',pv.create_pv,name='create_pv'),
    path('pv_detail/<str:pk>/',pv.pv_detail,name='pv_detail'),

    path('deletes_pvitems/<str:pk>/',pv.deletes_pvitems,name='deletes_pvitems'),
    path('manage_pv',pv.manage_pv,name='manage_pv'),
    path('pending_pv',pv.pending_pv,name='pending_pv'),
    path('view_pv/<str:pk>/',pv.view_pv,name='view_pv'),
    path('cancelled/<str:pk>/',pv.cancelled,name='cancelled'),
    path('approve/<str:pk>/',pv.approve,name='approve'),

    path('manage_payables',payerbles.manage_payables,name='manage_payables'),
    path('make_payment/<str:pk>/',payerbles.make_payment,name='make_payment'),

    path('manage_receivables',receivables.manage_receivables,name='manage_receivables'),


    path('students',student_bill.students,name='students'),
    path('list_active_academic_terms/<str:pk>/',student_bill.list_active_academic_terms,name='list_active_academic_terms'),
    path('create_bill/<str:academicterm_id>/<str:student_id>/',student_bill.create_bill,name='create_bill'),
    path('student_bill_details/<str:pk>/',student_bill.student_bill_details,name='student_bill_details'),
    path('manage_bills',student_bill.manage_bills,name='manage_bills'),
    path('view_student_bill/<str:pk>/',student_bill.view_student_bill,name='view_student_bill'),
    path('run_student_bills',student_bill.run_student_bills,name='run_student_bills'),
    path('deletes_billitems/<str:pk>/',student_bill.deletes_billitems,name='deletes_billitems'),


    path('manage_transfer',transfers.manage_transfer,name='manage_transfer'),
    path('edit_transfer/<str:pk>/',transfers.edit_transfer,name='edit_transfer'),
    path('cancel_tranfer/<str:pk>/',transfers.cancel_tranfer,name='cancel_tranfer'),
    path('comfirm_tranfer/<str:pk>/',transfers.comfirm_tranfer,name='comfirm_tranfer'),
    path('account_dashboards',account_dashboard.account_dashboards,name='account_dashboards'),

    path('manage_assets',fixed_assets.manage_assets,name='manage_assets'),
    path('apply_discount/<str:pk>/',student_bill.apply_discount,name='apply_discount'),

    path('void_pv/<str:pk>/',pv.void_pv,name='void_pv'),
    path('parent_see_bill',student_bill.parent_see_bill,name='parent_see_bill'),

    path('receive_payment/<str:pk>/',receivables.receive_payment,name='receive_payment'),
    path('sales',receivables.sales,name='sales'),
    path('student_account/<str:pk>/',receivables.student_account,name='student_account'),
    path('view_individual_bill/<str:pk>/<str:rec>/',receivables.view_individual_bill,name='view_individual_bill'),




]