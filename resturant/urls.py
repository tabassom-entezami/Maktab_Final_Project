from os import name
from django.urls import path
from .views import *

urlpatterns = [

    path('', home_page, name="Home"),
    path('foods/',resturant, name="store"),
	path('cart/', cart, name="cart"),
	path('product/<int:pk>/', product, name="product"),
    path('deleteitem/<int:pk>/',DeleteItem.as_view(),name ="deleteitem"),
    path('foodadd/', AddFoodPanelAdmin.as_view() , name = "addfood"),
    path('foodupdate/<int:pk>/', UpdateFoodPanelAdmin.as_view() , name = "updatefood"),
    path('fooddelete/<int:pk>/', DeleteFoodPanelAdmin.as_view() , name = "deletefood"),
    path('panel/', panel_admin , name ="paneladmin"),
    path('categoryadd/', AddCategoryPanelAdmin.as_view() , name = "addcategory"),


    
]
