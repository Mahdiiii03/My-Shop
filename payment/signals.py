from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ShippingAddress, Order
import datetime


@receiver(post_save, sender=User)
def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        ShippingAddress.objects.create(user=instance)


@receiver(pre_save, sender=Order)
def set_shipped_time(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now
