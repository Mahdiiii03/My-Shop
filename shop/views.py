from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Product, Category, Profile
from payment.models import ShippingAddress
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegistrationForm, ChangeUserInfoForm, ChangePasswordForm, ChangeUserProfForm
from payment.forms import ShippingForm
from django.contrib import messages
from django.db.models import Q
from cart.cart import Cart
import json
from django.http import JsonResponse


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def about(request):
    return render(request, 'about.html')


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                cart = Cart(request)
                current_profile = Profile.objects.get(user__id=request.user.id)
                old_cart = current_profile.old_cart
                if old_cart:
                    old_cart_dic = json.loads(old_cart)
                    for key, value in old_cart_dic.items():
                        cart.db_add(key, value)
                messages.success(request, 'you are now logged in (^^)')
                return redirect('home')
            else:
                messages.error(request, 'invalid username or password #_#')
                return redirect('login')


def logout_view(request):
    logout(request)
    messages.success(request, 'you are now logged in (^^)')
    return redirect('login')


def register_view(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'you are registered successfully! (^^)')
            return redirect('change_prof')
        else:
            messages.error(request, 'something went wrong #_#')
            return redirect('register')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})


def category_detail(request, cat):
    cat = cat.replace('-', ' ')
    categories = Category.objects.all()
    try:
        category = Category.objects.get(name=cat)
        products = category.products.all()
        return render(request, 'category.html', {'products': products, 'category': cat, 'categories': categories})
    except:
        messages.error(request, 'Category does not exist :(')
        return redirect('home')


def change_user(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'GET':
            form = ChangeUserInfoForm(instance=user)
            return render(request, 'registration/change_prof.html', {'form': form})
        if request.method == 'POST':
            form = ChangeUserInfoForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                login(request, user)
                messages.success(request, "information's updated successfully (^^)")
                return redirect('home')
    else:
        return render(request, 'registration/change_prof.html', {'form': ChangeUserInfoForm()})


def change_prof(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user__id=request.user.id)
        shipping_address = ShippingAddress.objects.get(user__id=request.user.id)

        if request.method == 'GET':
            form = ChangeUserProfForm(instance=profile)
            shipping_form = ShippingForm(instance=shipping_address)
            return render(request, 'registration/change_info.html', {'form': form, 'shipping_form':shipping_form})
        if request.method == 'POST':
            form = ChangeUserProfForm(request.POST or None, instance=profile)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_address)
            if form.is_valid() or shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, "profile updated successfully (^^)")
                return redirect('home')
    else:
        return render(request, 'registration/change_info.html', {'form': ChangeUserProfForm(),'shipping_form':ShippingForm()})


def change_password(request):
    user = request.user
    if request.user.is_authenticated:

        if request.method == 'GET':
            form = ChangePasswordForm(user)
            return render(request, 'registration/change_pass.html', {'form': form})
        if request.method == 'POST':
            form = ChangePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                login(request, user)
                messages.success(request, "password changed successfully (^^)")
                return redirect("change_user")
            else:
                for err in list(form.errors.values()):
                    messages.error(request, err)
                    return redirect('change_password')

    else:
        messages.error(request, 'login first :(')
        form = ChangePasswordForm(user)
        return render(request, 'registration/change_pass.html', {'form': form})


def search_home(request):
    searched = request.POST.get('search_home')
    products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

    categories = Category.objects.all()
    if products.count() > 0:
        return render(request, 'home.html', {'products': products, 'categories': categories})
    else:
        messages.success(request, "No products found try again :(")
        return render(request, 'home.html', {'products': None, 'categories': categories})
