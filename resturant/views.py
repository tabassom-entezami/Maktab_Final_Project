from django.db import models
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import *
from accounts.models import *
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import *
from django.contrib.auth.decorators import login_required


# @login_required
def home_page(re):
    return render(re, "Home.html")
# Create your views here.




def resturant(request):
	products = FoodMenu.objects.all()
	food = Food.objects.all()
	
	context = {'products':products,"food":food}
	return render(request, 'resturant.html', context)

def product(request, pk):
	product = FoodMenu.objects.get(id=pk)
	food = Food.objects.get(id=pk)
	if request.method == 'POST':
		product = FoodMenu.objects.get(id=pk)
		
		#Get user account information
		try:
			customer = request.user.customer
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(device=device)

		order, created = Order.objects.get_or_create(customer_id=customer, status="Order")
		orderItem, created = OrderItem.objects.get_or_create(order_id=order, food_menu_id=product)
		orderItem.number =request.POST['number']
		orderItem.save()

		return redirect('cart')

	context = {'product':product, "food":food }
	return render(request, 'product.html', context)

def cart(request):
	orderitems=OrderItem.objects.filter(order_id__isnull=False)
	food = Food.objects.filter(food__foodmenu__order_id__isnull=False)
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device=device)

	order, created = Order.objects.get_or_create(customer_id=customer, status="Order")

	context = {'order':order,"orderitems": orderitems,"food":food}
	return render(request, 'cart.html', context)