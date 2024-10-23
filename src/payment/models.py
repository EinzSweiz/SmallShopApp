from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

User = get_user_model()



class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    street_address =  models.CharField(max_length=100)
    apartament = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'ShippingAddress object' + str(self.id)
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


    def __str__(self):
        return 'Order' + str(self.id)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'OrderItem' + str(self.id)