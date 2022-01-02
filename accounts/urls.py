from django.urls import path
from .views import *

urlpatterns = [ 
    path('signup/', SignUpView.as_view(), name='signup'), 
    path('signupmanager/', SignUpManagerView.as_view(), name='signupmanager'), 
    # path('login/',LoginView.as_view(),name="login")
    ]