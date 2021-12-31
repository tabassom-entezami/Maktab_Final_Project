from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm ,PasswordChangeForm
from django.urls import reverse_lazy 
from django.views import generic
from .forms import *
# Create your views here.
class SignUpView(generic.CreateView): 
    form_class = CostumRegisterForm 
    success_url = reverse_lazy('Home') 
    template_name = 'registration/signup.html'