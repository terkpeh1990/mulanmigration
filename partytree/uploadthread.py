import threading
from django.http import request
from .models import *
from django.contrib import messages
from django.shortcuts import redirect,render
from django.utils.datastructures import MultiValueDictKeyError
from .models import *
from .forms import *



class  ProductThread(threading.Thread):
    def __init__(self, data):
        self.data= data

        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:

            for l in self.data['product']:
                d = Products.objects.filter(name=l[1])

                if d.exists():
                    # restock =Inventory_recordss.objects.create(product=d,quantity=l[4],status = 'Incoming')
                    # inventory =Inventorys.objects.create(product_id=d,instock = 0,unit_price=d.unit_price)
                    # inventory.instock +=l[4]
                    # inventory.save()
                    # print(d.name + " " +"Created")
                    # print(restock.product.name + " " +"restocked" + " "+ str(restock.quantity))
                    pass

                else:
                    try:
                        cats=Categorys.objects.get(name=l[2])
                    except Categorys.DoesNotExist:
                        cats=Categorys.objects.create(name=l[2])
                    product=Products.objects.create(id=l[0],name=l[1],category=cats,unit_price=l[3])
                    restock =Inventory_recordss.objects.create(product=product,quantity=l[4],status = 'Incoming')
                    inventory =Inventorys.objects.create(product_id=product,instock = 0,unit_price=product.unit_price)
                    inventory.instock +=l[4]
                    inventory.save()
                    inventory.avialable_stock_cost= product.unit_price * inventory.instock
                    print(product.name + " " +"Created")
                    print(restock.product.name + " " +"restocked" + " "+ str(restock.quantity))

        except IOError:
            print('fail')
            pass


class  RestockThread(threading.Thread):
    def __init__(self, data):
        self.data= data

        threading.Thread.__init__(self)

    def run(self):
        print('started')
        try:

            for l in self.data['product']:

                d = Products.objects.get(name=l[1])
                # restock =Inventory_recordss.objects.create(product=d,quantity= l[5],status = 'Incoming')

                inventory =Inventorys.objects.get(product_id=d.id)
                inventory.instock -=l[5]
                inventory.save()
                inventory.avialable_stock_cost= d.unit_price * inventory.instock
                print(d.name + " " +"Created")
                print(d.name + " " +"adjusted" + " "+ str(inventory.instock))

        except IOError:
            print('fail')
            pass