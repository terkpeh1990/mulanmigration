from django.contrib import messages
from django.shortcuts import redirect,render
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from .models import *
from .forms import *
from .uploadthread import *
from django.contrib.auth.decorators import login_required

def uploads_products(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                excel_file = form.cleaned_data['file']
                print (excel_file.name)
            except MultiValueDictKeyError:
                messages.success(request, "Error")
                return redirect('partytree:uploads_products')
            try:
                if (str(excel_file).split('.')[-1] == "xls"):
                    data = xls_get(excel_file,column_limit=8)
                    print('t')
                    ProductThread(data).start()
                elif (str(excel_file).split('.')[-1] == "xlsx"):
                    data = xlsx_get(excel_file,column_limit=8)
                    ProductThread(data).start()
                    print('is working')
                messages.success(request, "Upload Started")
                return redirect('partytree:manage_product')
            except IOError:
                print('fail')
                pass
                messages.success(request, "Upload Failed")
                return redirect('partytree:manage_product')
    else:
        form = UploadFileForm()

    template = 'partytree/upload.html'
    context= {
        'form':form,}
    return render(request,template,context)

def restock_products(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                excel_file = form.cleaned_data['file']
                print (excel_file.name)
            except MultiValueDictKeyError:
                messages.success(request, "Error")
                return redirect('partytree:restock_products')
            try:
                if (str(excel_file).split('.')[-1] == "xls"):
                    data = xls_get(excel_file,column_limit=8)
                    print('t')
                    RestockThread(data).start()
                elif (str(excel_file).split('.')[-1] == "xlsx"):
                    data = xlsx_get(excel_file,column_limit=8)
                    RestockThread(data).start()
                    print('is working')
                messages.success(request, "Upload Started")
                return redirect('partytree:manage_inventory')
            except IOError:
                print('fail')
                pass
                messages.success(request, "Upload Failed")
                return redirect('partytree:manage_restock')
    else:
        form = UploadFileForm()

    template = 'partytree/upload.html'
    context= {
        'form':form,}
    return render(request,template,context)