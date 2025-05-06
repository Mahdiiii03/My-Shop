from django.db import models
import datetime
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)
    description = models.TextField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default='', blank=True)
    quantity = models.IntegerField(default=1)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.customer} - {self.date}"
