from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product
from django.http import JsonResponse
from .cart import Cart
from django.contrib import messages


def cart_summery(request):
    cart = Cart(request)
    products = cart.get_products()
    quantity = cart.cart
    total = cart.get_total()
    return render(request, 'cart_summery.html', {'products': products,
                                                 'quantity': quantity, 'total': total})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, product_qty)
        cart_number = cart.__len__()
        response = JsonResponse({'cart_number': cart_number})
        messages.success(request, 'product added to cart successfully!(^^)')
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id)
        response = JsonResponse({"product_id": product_id})
        messages.success(request, 'product deleted successfully!(^^)')
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty')
        product = get_object_or_404(Product, id=product_id)
        cart.update(product, product_qty)
        response = JsonResponse({"product_id": product_id})
        messages.success(request, "your cart updated successfully! (^^)")
        return response

        # return redirect(cart_summery)


def search_cart(request):
    search = request.POST.get('search_cart')
    cart = Cart(request)
    products = cart.search_products(search)
    quantity = cart.cart
    total = cart.get_total()
    return render(request, 'cart_summery.html', {'products': products,
                                                 'quantity': quantity, 'total': total})
