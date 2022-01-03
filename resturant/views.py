from django.db import models
from django.db.models.expressions import OrderBy
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView 
from .models import *
from accounts.models import *
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import *
from django.urls import reverse_lazy
# @login_required
def home_page(re):
	products = FoodMenu.objects.all().filter(number__gt=0)
	food = Food.objects.all()

	# best_foods = []
	best_foods=( Food.objects.all().filter(food__foodmenu__order_id__status = "Delivery"))
	# best = OrderItem.objects.all().filter(order_id__status = "Send").annotate(Count('number')).order_by("-number__count")[:3]
	
	foods_deliverd=( Food.objects.all().filter(food__foodmenu__order_id__status = "Delivery"))
	order_item_of_one_food ={}
	for i in foods_deliverd:
		name = i.name
		order_item_of_one_food= OrderItem.objects.all().filter(food_menu_id__food_id__name = name).aggregate(Count("number"))
		# best_foods = dict(sorted(order_item_of_one_food.items(), key=lambda item: item[1]))


	
	context = {'products':products,"food":food,"best_foods":best_foods}
	return render(re, "Home.html" , context)
# Create your views here.

    	

@api_view(['POST'])
def foodUpdate_paneladmin(request, pk):
    food = Food.objects.get(id=pk)
    serializer = FoodSerilizer(instance=food, data=request.data)

    if serializer.is_valid():
        serializer.save()
        api_root = reverse_lazy('logout', request=request)
    return Response(serializer.data)

class DeleteItem(DeleteView):
	model = OrderItem
	template_name = "deletefood.html"
	success_url = reverse_lazy("cart")

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

		if ((FoodMenu.objects.all().filter(id = pk).values_list('number').last())[0]>= int(request.POST['number']) and (FoodMenu.objects.all().filter(id = pk).values_list('branch_id'))):
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
		
	# order, created = Order.objects.get_or_create(customer_id=customer,status="Order")

	context = {'order':orders,"orderitems": orderitems,"food":food,"orders":orders}
	return render(request, 'cart.html', context)