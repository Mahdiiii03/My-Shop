from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

admin.site.register(ShippingAddress)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'full_name',
        'email',
        'shipping_address',
        'amount_paid',
        'date_ordered',
        'shipped',
        'date_shipped',
    )
    list_filter = ('user', 'date_ordered')
    inlines = [OrderItemInline]
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped",
              "date_shipped"]
