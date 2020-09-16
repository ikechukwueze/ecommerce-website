from django.db import models
from django.conf import settings

# Create your models here.

from django.contrib.auth.models import User

from PIL import Image


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    stock = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)
    
    #image = ResizedImageField(size=[640, 360], upload_to=settings.MEDIA_ROOT)

    def __str__(self):
        return self.name

    
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            #new_height = 360
            #new_width = int(img.width * new_height / img.height)
            #print(new_width, new_height)
            
            #output_size = (new_width, new_height)
            output_size = (640, 360)
            img_r = img.resize(output_size)
            print(img_r.size)
            img_r.save(self.image.path)
    """        

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = settings.MEDIA_URL + 'placeholder.png'
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def getcartTotal(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.getTotal for item in orderitems])
        return total

    
    @property
    def getcartItems(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def getTotal(self):
        total = self.product.price * self.quantity
        return total


    def save(self, *args, **kwargs):
        if self.product:
            ordered_product = Product.objects.get(name=self.product)
            print(ordered_product.stock)
            #ordered_product_stock = ordered_product.stock
            if ordered_product.stock > self.quantity:
                ordered_product.stock -= self.quantity
                ordered_product.save() 
                print(ordered_product.stock)
                super().save(*args, **kwargs)



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=400, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address