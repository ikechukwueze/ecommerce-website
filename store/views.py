from django.shortcuts import render
from .models import *
from django.conf import settings

from django.http import JsonResponse
import json
# Create your views here.



def store(request):
    products = Product.objects.all()
    data = {'products':products}

    return render(request, 'store/store.html', data)




def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'getcartItems':0, 'getcartTotal':0}
    
    data = {'items':items, 'order':order}
    return render(request, 'store/cart.html', data)





def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'getcartItems':0, 'getcartTotal':0}
    
    data = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', data)





def updateItem(request):

    body = request.body.decode('utf-8')
    
    data = json.loads(body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
        product.stock -= 1

    
    elif action == 'remove':
        orderItem.quantity -= 1
        product.stock += 1
        
    

    
    orderItem.save()
    product.save()
    items_in_cart = order.getcartItems
    print(items_in_cart )
 

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse(items_in_cart, safe=False)
    