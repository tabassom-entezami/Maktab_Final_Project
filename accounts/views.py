
from django.contrib.auth.forms import UserCreationForm ,PasswordChangeForm
from django.urls import reverse_lazy 
from django.views import generic
from .forms import *
# Create your views here.
from django.shortcuts import  render, redirect
from django.contrib import messages
from django.views.generic.edit import DeleteView,CreateView,UpdateView
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password )
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("Home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("Home")


class SignUpView(generic.CreateView): 
    form_class = CostumRegisterForm 
    success_url = reverse_lazy('Home') 
    template_name = 'registration/signup.html'

class SignUpManagerView(generic.CreateView):
    form_class = CostumRegisterForm1 
    success_url = reverse_lazy('Home') 
    template_name = 'registration/signupmanager.html'


class LoginView(generic.CreateView): 
    form_class = CostumRegisterForm 
    success_url = reverse_lazy('Home') 
    template_name = 'registration/login.html'


class AddressCreate(CreateView):
    model = CustomerAdress
    template_name = "address.html"
    success_url = reverse_lazy('cart')
    fields = "__all__"

