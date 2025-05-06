from django.contrib import admin
from . import models
from django.contrib.auth.models import User


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer',)
@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

class profileInline(admin.StackedInline):
    model = models.Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', ]
    inlines = [profileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models.Category)
