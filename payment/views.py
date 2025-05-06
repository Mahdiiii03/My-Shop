from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem
from django.forms.models import model_to_dict
from django.contrib import messages
from .forms import PaymentForm
from shop.models import Profile


# Create your views here.
def checkout(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        products = cart.get_products()
        orders = cart.cart
        total = cart.get_total()
        shipping_address = ShippingAddress.objects.get(user__id=request.user.id)
        ship_add = model_to_dict(shipping_address)

        payment_form = PaymentForm()
        return render(request, 'payment.html',
                      {"products": products, "orders": orders, "total": total, "shipping_add": ship_add,
                       "payment_form": payment_form})
    else:
        messages.success(request, "Access denied Login First...")
        return redirect("home")


def process_order(request):
    if request.method == "POST":

        cart = Cart(request)
        products = cart.get_products()
        orders = cart.cart
        total = cart.get_total()

        shipping = ShippingAddress.objects.get(user__id=request.user.id)
        full_name = shipping.shipping_fullname
        email = shipping.shipping_email

        shipping_address = f"{shipping.shipping_address1}\n{shipping.shipping_address2}\n{shipping.shipping_city}, {shipping.shipping_state}\n{shipping.shipping_country}"
        amount_paid = total
        # Create an Order
        if request.user.is_authenticated:
            # Logged in
            user = request.user
            # Create order
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk

            # Get product info
            for product in products:
                # Get product ID
                product_id = product.id
                # Get product price
                if product.sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get quantity
                for key, value in cart.cart.items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]
                # Delete Cart from Database (old cart field)
                current_user = Profile.objects.filter(user__id=request.user.id)
                # Delete shopping cart in db
                current_user.update(old_cart="")

                messages.success(request, 'order created')
                return redirect('home')
    else:
        messages.warning(request, "Access Denied!")
        return redirect("home")


def shipped_order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.method == "POST":
            order_id = request.POST['num']
            order = Order.objects.filter(id=order_id)
            order.update(shipped=False)
            messages.success(request, "Shipping status updated!")
            return redirect("home")
        return render(request, 'shipped.html', {"orders": orders})
    else:
        messages.success(request, "Order Shipped!")
        return redirect("home")


def unshipped_order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.method == "POST":
            order_id = request.POST['num']
            order = Order.objects.filter(id=order_id)
            order.update(shipped=True)
            messages.success(request, "Shipping status updated!")
            return redirect("home")

        return render(request, 'unshipped.html', {"orders": orders})
    else:
        messages.success(request, "Order Requires Shipping!")
        return redirect("home")


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=pk)
        if request.method == "POST":
            status = request.POST['shipping_status']
            if status == "true":
                order.shipped = True
                order.save()
            else:
                order.shipped = False
                order.save()
            messages.success(request, "Shipping status updated!")
            return redirect("home")
        return render(request, 'order.html', {"order": order, "items": order_items})
    else:
        messages.warning(request, "Access Denied!")
        return redirect("home")
