from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .forms import *
from .models import *
from .filters import *
from twilio.rest import TwilioRestClient
from twilio.rest import Client
from school_management_system.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView
from django.views.generic.edit import CreateView
from django.core import serializers
from twilio.rest import Client


def Billtype(request):
    if request.method == 'POST':
        form = Biling_TypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Billing type added successfully')
            return redirect('school:managebilltype')
    else:
        form = Biling_TypeForm()
    template = 'billing/create_billtype.html'
    context = {
        'form': form,
        }
    return render(request, template, context)

def edit_billtype(request,pk):
    bill_type = Billing_type.objects.get(id=pk)
    if request.method == 'POST':
        form = Biling_TypeForm(request.POST, instance=bill_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billing type added successfully')
            return redirect('school:managebilltype')
    else:
        form = Biling_TypeForm(instance=bill_type)
    template = 'billing/create_billtype.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

def managebilltype(request):
    types = Billing_type.objects.all()
    template = 'billing/manage_billtype.html'
    context = {
        'types': types,
    }
    return render(request, template, context)


def create_bill(request, pk):
    student = Students.objects.get(id=pk)
    if request.method == 'POST':
        form=BillingForm(request.POST)
        if form.is_valid():
            bb=form.save(commit = False)
            bb.student_id = student
            # parent  = Parents.objects
            bb.parent_id = student.parent_id
            student.bills = True
            bb.save()
            # student.bills=True
            student.save()
            messages.success(request, 'Bill Created. Please Proceed to add details')
            request.session['id'] = bb.id
            return redirect('school:Billitems')
    else:
        form = BillingForm()
    template = 'billing/create_bill.html'
    context = {
        'student': student,
        'form': form,
        }
    return render(request, template, context)


class Billitems(CreateView):
    model = Billing_details
    form_class = Bill_detailForm
    template = 'billing/add_bill_details.html'

    def get(self, *args, **kwargs):
        if self.request.session['id']:
            bill_id = self.request.session['id']
            bills = Billing.objects.get(id=bill_id)
            student = Students.objects.get(id=bills.student_id)
            form = self.form_class()
            detail = Billing_details.objects.filter(billing_id=bills)
            bills.save()
            return render(self.request, self.template, {"form": form, "detail": detail, "bills": bills})

    def post(self,  *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if self.request.session['id']:
                bill_id = self.request.session['id']
                student_bill = Billing.objects.get(id=bill_id)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.billing_id = student_bill
                instance.save()
                student_bill.total += instance.amount
                student_bill.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self, form):
        messages.success(self.request, 'Bill item added')
        return super().form_valid(form)


def delete_bill_item(request,pk):
    item = Billing_details.objects.get(id=pk)
    bill = Billing.objects.get(id=item.billing_id.id)
    bill.total-=int(item.amount)
    bill.save()
    item.delete()
    messages.success(request, 'Bill item deleted')
    return redirect('school:Billitems')

def delete_bill(request,pk):
    item = Billing.objects.get(id=pk)
    item.delete()
    messages.success(request, 'Bill item deleted')
    return redirect('school:manage_bills')

def close_billss(request):
    if request.user.profile.is_parent:
        return redirect('school:parent_bills')
    else:
        return redirect('school:manage_bills')

def manage_bills(request):
    studbills = Billing.objects.filter()
    template = 'billing/manage_bills.html'
    context = {
        'studbills': studbills,
    }
    return render(request, template, context)



def parent_bills(request):
    parent = Parents.objects.get(id=request.user.username)
    studbills = Billing.objects.filter(balance__gt=0,parent_id = parent.id)
    template = 'billing/manage_bills.html'
    context = {
        'studbills': studbills,
    }
    return render(request, template, context)


def close_bill(request):
    if request.session['id']:
        try:
            # studbill = Billing.objects.get(id=request.session['id'])
            # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # if studbill.billing_type.name == 'School Fees':
            #     try:
            #         message = client.messages.create(
            #             to="+233" + studbill.student_id.parent_id.father_phone,
            #             from_=TWILIO_PHONE_NUMBER,
            #             body="Dear" + " " + studbill.student_id.parent_id.father_name + "," + " " + "The total all inclusive MSAC package for your ward " + " " + studbill.student_id.Surname + " "+studbill.student_id.firstname + " for the" + " " + studbill.term_year_id.name + " "+"is " + " " + "GHC" + " " + str(studbill.total) + "." + "\nPlease note, all parents will be required to make 70% payment  of the total bill for the term before their ward starts school on the 13/09/2021." + "\nMSAC administration is opened from yhe 6/09 - 10/09." + "\n\n All payment should be made to the bank details below :-" + "\n\nUMB (legon branch)"+"\nA/C numb :- 0321546688012"+"\n\nOMNIBSIC ( East legon branch)"+"\nA/C :- 100323028000"+"\n\nPayment reference should be in your wards name."+"\nFor further enquiries, kindly contact the admissions office on 0302985321 or 0207771025")
            #     except IOError:
            #         print('fail')
            #         pass
            #     try:
            #         message = client.messages.create(
            #             to="+233" + studbill.student_id.parent_id.mother_phone,
            #             from_=TWILIO_PHONE_NUMBER,
            #             body="Dear" + " " + studbill.student_id.parent_id.mother_name + "," + " " + "The total all inclusive MSAC package for your ward " + " " + studbill.student_id.Surname + " "+studbill.student_id.firstname + " for the" + " " + studbill.term_year_id.name + " "+"is " + " " + "GHC" + " " + str(studbill.total) + "." + "\nPlease note, all parents will be required to make 70% payment  of the total bill for the term before their ward starts school on the 13/09/2021." + "\nMSAC administration is opened from yhe 6/09 - 10/09." + "\n\nAll payment should be made to the bank details below :-" + "\n\nUMB (legon branch)"+"\nA/C numb :- 0321546688012"+"\n\nOMNIBSIC ( East legon branch)"+"\nA/C :- 100323028000"+"\n\nPayment reference should be in your wards name."+"\nFor further enquiries, kindly contact the admissions office on 0302985321 or 0207771025")

            #     except IOError:
            #         print('fail')
            #         pass
            del request.session['id']
            return redirect('school:studlist')
            # else:
            #     print('test')
            #     return redirect('school:studlist')
        except KeyError:
            return redirect('school:studlist')

def studlist(request):
    std = Students.objects.all()


    template = 'billing/student_list.html'

    context = {

        'std': std,

    }
    return render(request, template, context)


def view_bills(request,pk):
    std = Billing.objects.get(id=pk)
    std_bill = Billing_details.objects.filter(billing_id=std.id)

    history = Payment_History.objects.filter(billing_id=std.id)

    template = 'billing/view_bill.html'

    context = {

        'std': std,
        'std_bill': std_bill,
        'history': history,
    }
    return render(request, template, context)


@login_required
def make_payment(request, pk):
    st = Billing.objects.get(id=pk)
    if request.method == "POST":
        form = paymentform(request.POST)
        if form.is_valid():
            amount_paid = form.cleaned_data['amount_paid']
            cc = amount_paid + st.amount_paid
            percentage = int(float(st.total) * 0.7)
            if cc >= percentage:
                st.amount_paid += amount_paid
                st.save()
                Payment_History.objects.create(billing_id=st, amount_paid=amount_paid)
                if st.billing_type.name =='School Fees':
                    acc = Account_code.objects.get(code="School Fees")
                elif st.billing_type.name == 'Summer School':
                    acc = Account_code.objects.get(code="Summer School")
                elif st.billing_type.name == 'Pickup and Drop Off (School Bus)' or st.billing_type.name == 'Pickup (School Bus)' or st.billing_type.name == 'Drop Off (School Bus)':
                    acc = Account_code.objects.get(code="School Bus")
                elif st.billing_type.name == 'Weekly Drop Off Kids' or st.billing_type.name == 'Monthly Drop Off Kids' or st.billing_type.name == 'Half Day Drop Off Kids' or st.billing_type.name == 'Biweekly Drop Off Kids' or st.billing_type.name == '1 Hour Drop Off kids':
                    acc = Account_code.objects.get(code="Drop Off")
                elif st.billing_type.name == 'After School Care':
                    acc = Account_code.objects.get(code="After School Care")
                elif st.billing_type.name == 'Special Education Needs Fees':
                    acc = Account_code.objects.get(code="Special Education Needs Fees")
                elif st.billing_type.name == 'Speech':
                    acc = Account_code.objects.get(code="Speech")
                elif st.billing_type.name == 'UCMAS':
                    acc = Account_code.objects.get(code="UCMAS")
                elif st.billing_type.name == 'Weekend Care':
                    acc = Account_code.objects.get(code="Weekend Care")
                else:
                    acc = Account_code.objects.get(code="School Fees")
                company = Company_group.objects.get(name="Mulan")
                Revenue.objects.create(
                    account_code=acc, amount=amount_paid, company=company)
                messages.success(request, "Payment Made Successfully")
                return redirect('school:manage_bills')
            else:
                messages.success(request, "Payment Decliend!!, Payment must be more than 70%"+ " "+ "of total bill which is"+ " "+ str(percentage) )
                return redirect('school:make_payment',pk=st.id)

    else:
        form = paymentform()

    context = {
        'form': form,
    }
    template = 'billing/payment.html'
    return render(request, template, context)
