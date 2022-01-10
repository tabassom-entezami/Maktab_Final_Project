
from django.urls import reverse_lazy 
from django.views import generic
from .forms import *
from .models import *
from django.db.models import Q
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


def sign_up_view(request):
    form = CostumRegisterForm()
    if request.method == "POST":
        form = CostumRegisterForm(request.POST)
        if form.is_valid():
            form = form.save()

            customer = Customer.objects.get(username = request.POST["username"] )
            address ,create= Address.objects.get_or_create(city = request.POST["city"],street =request.POST["street"],plaque = request.POST["plaque"])
            address.save()
            customeraddress ,create= CustomerAdress.objects.get_or_create(customer = customer,address=address,default = True)
            customeraddress.save()
            return redirect("Home")
    return render(request , "registration/signup.html" , {"form":form})

def sign_up_manager_view (request):
    form = CostumRegisterForm1()
    if request.method == "POST":
        form = CostumRegisterForm1(request.POST)
        if form.is_valid() and request.POST["password"] and request.POST["password2"] and request.POST["password"] == request.POST["password2"]:
            form = form.save()
            return redirect("Home")
        return render(request , "registration/signupmanager.html" , {"form":form,"msg":"something went wrong"})

    return render(request , "registration/signupmanager.html" , {"form":form})


class LoginView(generic.CreateView): 
    form_class = CostumRegisterForm 
    success_url = reverse_lazy('Home') 
    template_name = 'registration/login.html'



def address_create(request):
    if request.method == 'POST':
        city = request.POST['city']
        street = request.POST['street']
        plaque = request.POST['plaque']
        is_it = request.POST["it_is"]

        device = request.COOKIES['device']
        customer = request.user
        customer  = Customer.objects.get(email = customer.email)
        address  = Address.objects.create(city = city,street = street,plaque=int(plaque))
        if is_it == "True":
            edit , create = CustomerAdress.objects.filter(customer__email = customer.email).get_or_create(default =True)
            edit.default = False
            edit.save()
            customeraddress = CustomerAdress.objects.create(customer = customer , address = address,default=True)
        else:
            customeraddress = CustomerAdress.objects.create(customer = customer , address = address,default=False)
        return redirect("cart")
    return render(request , "address.html")


