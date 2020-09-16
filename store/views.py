from django.shortcuts import render
from .models import *
from django.conf import settings
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
    
    data = {'items':items, 'order':order}
    return render(request, 'store/cart.html', data)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
    
    data = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', data)