from os import name
from django.urls import path
from .views import *

urlpatterns = [

    path('', home_page, name="Home"),
    path('foods/',resturant, name="store"),
	path('cart/', cart, name="cart"),
	path('product/<str:pk>/', product, name="product"),
    
]