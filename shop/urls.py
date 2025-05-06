from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('product/<int:pk>', views.product_detail, name='product'),
    path('category/<str:cat>', views.category_detail,name='category'),
    path('change-user', views.change_user,name='change_user'),
    path('change-prof', views.change_prof,name='change_prof'),
    path('change-pass', views.change_password,name='change_password'),
    path('search_home', views.search_home,name='search_home'),
]
