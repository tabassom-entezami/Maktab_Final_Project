from django.urls import path
from .views import *

urlpatterns = [ 
    path('signup/',sign_up_view , name='signup'), 
    path('signupmanager/', sign_up_manager_view, name='signupmanager'), 
    path("login/", login_request , name="login"),
    path("addaddress/",address_create,name = "addaddress"),
    path("logout/", logout_request, name= "logout"),


    
    ]