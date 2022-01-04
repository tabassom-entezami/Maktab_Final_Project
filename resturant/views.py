from django.db import models
from django.db.models.expressions import OrderBy
from django.db.models.aggregates import Count, Sum
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView,CreateView,UpdateView
from resturant.forms import *
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
	# food = Food.objects.all()

	# best_foods = []
	#  best_foods=( Food.objects.all().filter(food__foodmenu__order_id__status = "Delivery"))
	# best = OrderItem.objects.all().filter(order_id__status = "Send").annotate(Count('number')).order_by("-number__count")[:3]
	
	foods_deliverd= Food.objects.all().filter(food__foodmenu__order_id__status = "Peyment")
	my_dict ={}
	for i in foods_deliverd:
		name = i.name
		order_item_of_one_food= OrderItem.objects.all().filter(food_menu_id__food_id__name = name).aggregate(Count("number"))["number__count"]
		# print(order_item_of_one_food)
		my_dict.update({i:order_item_of_one_food})
	best_foods = dict(sorted(my_dict.items(), key=lambda item: item[1]))

	values = Food.objects.all().filter(food__foodmenu__order_id__status = "Peyment").annotate(our_sum=Sum("food__foodmenu__number")).order_by("-our_sum")[:3]



	context = {'products':products,"way2":best_foods,"best_foods":values}
	return render(re, "Home.html" , context)
# Create your views here.



def panel_admin(req):
	foods = Food.objects.all()
	content = {"foods": foods}
	return render(req,"paneladmin.html",content)



class AddFoodPanelAdmin(CreateView):
	model = Food
	success_url = reverse_lazy("paneladmin")
	template_name = "addfood.html"
	fields = "__all__"

class AddCategoryPanelAdmin(CreateView):
	model = Category
	success_url = reverse_lazy("paneladmin")
	template_name = "addcategory.html"
	fields = "__all__"

class UpdateFoodPanelAdmin(UpdateView):
	model = Food
	success_url = reverse_lazy("paneladmin")
	template_name = "updatefood.html"
	fields = "__all__"

class DeleteFoodPanelAdmin(DeleteView):
	model = Food
	template_name = "deletefood.html"
	success_url = reverse_lazy("paneladmin")
	fields = "__all__"

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
		# product = FoodMenu.objects.get(id=pk)
		# flag = True
		#Get user account information
		try:
			customer = request.user.customer
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(device=device,username=device)
		# print(FoodMenu.objects.all().filter(id = pk).values_list('number').last()[0])

		if ((FoodMenu.objects.all().filter(id = pk).values_list('number').last())[0]>= int(request.POST['number'])):
			flag = True
			order, created = Order.objects.get_or_create(customer_id=customer, status="Order")
			orderItem, created = OrderItem.objects.get_or_create(order_id=order, food_menu_id=product, number = int(request.POST['number']))
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
 
	try:
		customer = request.user.customer
		device = request.COOKIES['device']
		orderitems=OrderItem.objects.filter(order_id__customer_id__username=customer.username)
		food = Food.objects.filter(food__foodmenu__order_id__customer_id__username=customer.username)
		orders = Order.objects.filter(customer_id__username=customer.username)
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device=device ,username = device)
		orderitems=OrderItem.objects.filter(order_id__customer_id__username=device)
		food = Food.objects.filter(food__foodmenu__order_id__customer_id__username=device)
		orders = Order.objects.filter(customer_id__username=device)
	# order, created = Order.objects.get_or_create(customer_id=customer,status="Order")

	context = {'order':orders,"orderitems": orderitems,"food":food}
	return render(request, 'cart.html', context)