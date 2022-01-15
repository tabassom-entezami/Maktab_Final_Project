
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
from resturant.models import *
from resturant.decorators import *
from django.contrib.auth.decorators import login_required 


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

@login_required
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
            return redirect("login")
    return render(request , "registration/signup.html" , {"form":form})

def sign_up_manager_view (request):
    form = CostumRegisterForm1()
    if request.method == "POST":
        form = CostumRegisterForm1(request.POST)
        if form.is_valid() and request.POST["password"] and request.POST["password2"] and request.POST["password"] == request.POST["password2"]:
            form = form.save()
            return redirect("login")
        return render(request , "registration/signupmanager.html" , {"form":form,"msg":"something went wrong"})

    return render(request , "registration/signupmanager.html" , {"form":form})


class LoginView(CreateView): 
    form_class = CostumRegisterForm 
    success_url = reverse_lazy('Home') 
    template_name = 'registration/login.html'


@login_required
def address_create(request):
    if request.method == 'POST':
        city = request.POST['city']
        street = request.POST['street']
        plaque = request.POST['plaque']
        is_it = request.POST["it_is"]
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



@login_required
def delete_address(request,pk):
    if not(request.user.is_staff):
        context = {}
        context["orders"] = Order.objects.filter(customer_id__username = request.user.username)
        context["address"] = Address.objects.filter(customer_address__customer__username = request.user.username)
        if CustomerAdress.objects.filter(address__id = pk).values_list("default")[0][0] == True :
            context["msg"] = "this is your default address you can't remove it"
            return render(request,"customerPanel/customer_panel.html",context)
        else:
            address_to_remove = CustomerAdress.objects.get(address__id = pk)
            address_to_remove.delete()
            context["msg"] = "address deleted"
            return render(request,"customerPanel/customer_panel.html",context)
    else:
        return render(request,"customerPanel/customer_panel.html",{"msg":"you are not a customer"})

@login_required
def change_default_address(request,pk):
    if not(request.user.is_staff ):
        context = {}
        context["orders"] = Order.objects.filter(customer_id__username = request.user.username)
        context["address"] = Address.objects.filter(customer_address__customer__username = request.user.username)
        if CustomerAdress.objects.filter(address__id = pk).values_list("default")[0][0] != True :
            edit  = CustomerAdress.objects.filter(customer__username = request.user.username).get(default = True )
            edit.default = False
            edit.save()
            customeraddress = CustomerAdress.objects.get(address__id = pk)
            customeraddress.defualt = True
            customeraddress.save()
            context["msg"] ="your default change"
        else :
            context["msg"] =" it is your default!!!! "
        return render(request,"customerPanel/customer_panel.html",context)
    else:
        return render(request,"customerPanel/customer_panel.html",{"msg":"you are not a customer"})


        