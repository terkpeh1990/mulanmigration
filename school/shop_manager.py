from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .forms import *
from .models import *
from bakery.models import *
from partytree.models import *
from salon.models import *
from .filters import *
from twilio.rest import TwilioRestClient
from twilio.rest import Client
from school_management_system.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from django.utils.html import strip_tags

def managerdashboard(request):
    bakes = Company_group.objects.get(name = "Party Tree Bakes")
    party = Company_group.objects.get(name = "Party Tree")
    irish = Company_group.objects.get(name = "Irish Green")
    # object_status_list = ["Approved", "Issued"]
    today = datetime.datetime.now()
    monthlybakes_revenue = Revenue.objects.filter(company=bakes,
        created_date__year=today.year,created_date__month=today.month).aggregate(total_revenue=Sum('amount'))
    monthyparty_revenue = Revenue.objects.filter(company=party,
        created_date__year=today.year,created_date__month=today.month).aggregate(total_revenue=Sum('amount'))
    monthyirish_revenue = Revenue.objects.filter(company=party,
        created_date__year=today.year,created_date__month=today.month).aggregate(total_revenue=Sum('amount'))
    montlybakes_expenditure = Expenditure.objects.filter(company=bakes,
        created_date__year=today.year,created_date__month=today.month).aggregate(total_expenditure=Sum('amount'))
    montlyparty_expenditure = Expenditure.objects.filter(company=party,
        created_date__year=today.year,created_date__month=today.month).aggregate(total_expenditure=Sum('amount'))
    montlyirish_expenditure = Expenditure.objects.filter(company=irish,
        created_date__year=today.year,created_date__month=today.month).aggregate(total_expenditure=Sum('amount'))

    backery_receivable = Order.objects.all().aggregate(cc=Sum('balance'))
    irish_receivable = SalonOrder.objects.all().aggregate(cc=Sum('balance'))
    partytree_receivable = Orders.objects.all().aggregate(cc=Sum('balance'))
    bakes_orders = Order.objects.all()
    salonorders = SalonOrder.objects.all()
    partyorders = Orders.objects.all()

    template='hod_template/shop_manager.html'
    context ={

        'monthlybakes_revenue': monthlybakes_revenue,
        'monthyparty_revenue': monthyparty_revenue,
        'monthyirish_revenue': monthyirish_revenue,
        'montlybakes_expenditure':montlybakes_expenditure,
        'montlyparty_expenditure': montlyparty_expenditure,
        'montlyirish_expenditure':montlyirish_expenditure,
        'backery_receivable': backery_receivable,
        'irish_receivable': irish_receivable,
        'partytree_receivable': partytree_receivable,
        'bakes_orders':bakes_orders,
        'salonorders':salonorders,
        'partyorders':partyorders,

    }

    return render(request,template,context)
