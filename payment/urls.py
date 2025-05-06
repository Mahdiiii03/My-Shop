from django.urls import path
from . import views

urlpatterns = [
   path('check', views.checkout, name='checkout'),
   path('pay', views.process_order, name='pay'),
   path('shipped_orders', views.shipped_order, name='shipped'),
   path('unshipped_orders', views.unshipped_order, name='unshipped'),
   path('order <int:pk>', views.orders, name='order'),

]
