
from django.contrib.auth.forms import UserCreationForm ,PasswordChangeForm
from django.urls import reverse_lazy 
from django.views import generic
from .forms import *
# Create your views here.
from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages

# def register_request(request):
# 	if request.method == "POST":
# 		form = CostumRegisterForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			login(request, user)
# 			messages.success(request, "Registration successful." )
# 			return redirect("main:homepage")
# 		messages.error(request, "Unsuccessful registration. Invalid information.")
# 	form = CostumRegisterForm()
# 	return render (request=request, template_name="main/register.html", context={"register_form":form})
class SignUpView(generic.CreateView): 
    form_class = CostumRegisterForm 
    success_url = reverse_lazy('Home') 
    template_name = 'registration/signup.html'

class LoginView(generic.CreateView): 
    form_class = CostumRegisterForm 
    success_url = reverse_lazy('Home') 
    template_name = 'registration/login.html'


