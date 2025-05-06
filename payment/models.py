from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shipping_fullname = models.CharField(max_length=200, blank=True)
    shipping_phone = models.CharField(max_length=20, blank=True)
    shipping_address1 = models.CharField(max_length=200, blank=True)
    shipping_address2 = models.CharField(max_length=200, blank=True,null=True)
    shipping_email = models.EmailField(max_length=100, blank=True, null=True)
    shipping_city = models.CharField(max_length=200, blank=True)
    shipping_state = models.CharField(max_length=200, blank=True,null=True)
    shipping_country = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.shipping_fullname


class Order(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, blank=True,null=True)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'

# Create Order Items Model
class OrderItem(models.Model):
    # Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Order - {str(self.id)}'