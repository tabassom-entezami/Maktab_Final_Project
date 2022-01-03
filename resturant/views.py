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
	products = FoodMenu.objects.all().filter(number__gt=0)
	food = Food.objects.all()

	best_foods = []
	best_foods=( Food.objects.all().filter(food__foodmenu__order_id__status = "Send").values_list("name"))
	
	print(best_foods)
	context = {'products':products,"food":food,"best_foods":best_foods}
	return render(re, "Home.html" , context)
# Create your views here.




def resturant(request):
	products = FoodMenu.objects.all()
	food = Food.objects.all()
	
	context = {'products':products,"food":food}
	return render(request, 'resturant.html', context)

def product(request, pk):
	product = FoodMenu.objects.get(id=pk)
	food = Food.objects.get(food__id = pk)
	if request.method == 'POST':
		product = FoodMenu.objects.get(id=pk)
		# flag = True
		#Get user account information
		try:
			customer = request.user.customer
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(device=device,username=device)
		# print(FoodMenu.objects.all().filter(id = pk).values_list('number').last()[0])

		if ((FoodMenu.objects.all().filter(id = pk).values_list('number').last())[0]> int(request.POST['number']) and (FoodMenu.objects.all().filter(id = pk).values_list('branch_id'))):
			flag = True
			order, created = Order.objects.get_or_create(customer_id=customer, status="Order")
			orderItem, created = OrderItem.objects.get_or_create(order_id=order, food_menu_id=product)
			orderItem.number =request.POST['number']
			orderItem.save()
			# makeitcorrect =FoodMenu.objects.all().filter(id = pk).values_list('number').last()[0]  - int(request.POST['number'])
			# product.number = makeitcorrect
			# product.save()
			return redirect('cart')
		else:
				context = {'product':product, "food":food ,'msg':"we dont have enough"}
				return render(request, 'product.html', context)

	context = {'product':product, "food":food }
	return render(request, 'product.html', context)

def cart(request):# باید بعدا درست شه
	device = request.COOKIES['device']
	orderitems=OrderItem.objects.filter(order_id__customer_id__username=device)
	food = Food.objects.filter(food__foodmenu__order_id__customer_id__username=device)
	orders = Order.objects.filter(customer_id__username=device) # بعدا
	try:
		customer = request.user.customer

	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device=device ,username = device)
		
	order, created = Order.objects.get_or_create(customer_id=customer,status="Order")

	context = {'order':order,"orderitems": orderitems,"food":food,"orders":orders}
	return render(request, 'cart.html', context)