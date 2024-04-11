import os
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)

    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True) #display if the product is in digital format regarding shipping
    image = models.ImageField(upload_to="", null=True, blank=True, default="static/images/placeholder.png")

    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

@receiver(pre_save, sender=Product)
def SaveImages(sender, instance, **kwargs):
    if instance.image:
        folderName = slugify(f"{instance.name}")
        folderPath = os.path.join(settings.MEDIA_ROOT, 'product_images', folderName)

        # Create the folder if it doesn't exist
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        # Saveing the image inside the folder
        instance.image.name = os.path.join('product_images', folderName, instance.image.name)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    dateOrderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transactionId = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def getCartItems(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def getCartTotal(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.getTotal for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name
    
    @property
    def getTotal(self):
        total = self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address

