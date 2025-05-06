from shop.models import Product, Profile
from django.db.models import Q


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product_id, quantity):
        product_id = str(product_id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(quantity)
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_profile.update(old_cart=carty)

    def add(self, product, quantity):
        product_id = str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(quantity)
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_profile.update(old_cart=carty)

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def search_products(self, name):
        products = self.get_products()
        result = products.filter(Q(name__icontains=name) | Q(description__icontains=name))
        return result

    def get_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for key, value in self.cart.items():
            for product in products:
                key = int(key)
                if product.id == key:
                    if product.sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)
        return total

    def update(self, product, quantity):
        product_id = str(product.id)
        self.cart[product_id] = int(quantity)
        if self.request.user.is_authenticated:
            current_profile = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_profile.update(old_cart=carty)

        self.session.modified = True

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            if self.request.user.is_authenticated:
                current_profile = Profile.objects.filter(user__id=self.request.user.id)
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                current_profile.update(old_cart=carty)

        self.session.modified = True
