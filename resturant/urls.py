from os import name
from django.urls import path
from .views import *

urlpatterns = [

    path('', home_page, name="Home"),
    path('resturant/',store, name="store"),
	path('cart/', cart, name="cart"),
	path('product/<str:pk>/', product, name="product"),
    
]