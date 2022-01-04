from os import name
from django.urls import path
from .views import *

urlpatterns = [

    path('', home_page, name="Home"),
    path('foods/',resturant, name="store"),
	path('cart/', cart, name="cart"),
	path('product/<int:pk>/', product, name="product"),
    path('delete-item/<int:pk>',DeleteItem.as_view(),name = "delete-item"),
    path('food_id', food_add_panel_admin , name = "addfood"),
    path('food_form_add', webmanager,name = "manager")
    
]
