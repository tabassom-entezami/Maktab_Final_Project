from django.urls import path
from .views import *

urlpatterns = [ 
    path('signup/',sign_up_view , name='signup'), 
    path('signupmanager/', sign_up_manager_view, name='signupmanager'), 
    path("login/", login_request , name="login"),
    path("addaddress/",address_create,name = "addaddress"),
    path("logout/", logout_request, name= "logout"),
    path("change_address/<int:pk>/",change_default_address,name="change"),
    path("delete_address/<int:pk>/",delete_address,name="delete_address"),
    path("address_result/", address_result, name="address2"),
    path("<int:pk>/", get_info_address ,name="get_address") ,
    ]