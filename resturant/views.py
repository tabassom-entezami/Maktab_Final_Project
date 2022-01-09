from django.db import models
from django.db.models.expressions import OrderBy
from django.db.models.aggregates import Count, Sum
from django.db.models import Q
from django.db.models.fields import Field
from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView,CreateView,UpdateView 
from resturant.forms import *
from .models import *
from accounts.models import *
from django.views.decorators.http import require_POST
from .decorators import *
from django.views.generic import ListView
from accounts.models import *
from django.contrib.auth.decorators import login_required 
from django.db.models import Count 

from .serializer import *
from django.urls import reverse_lazy
# @login_required
def home_page(re):
	products = FoodMenu.objects.all().filter(number__gt=0)
	foods_deliverd= Food.objects.all().filter(food__foodmenu__order_id__status = "Peyment")
	branches = Branch.objects.all()
	my_dict ={}
	for i in foods_deliverd:
		name = i.name
		order_item_of_one_food= OrderItem.objects.all().filter(food_menu_id__food_id__name = name).aggregate(Count("number"))["number__count"]
		
		my_dict.update({i:order_item_of_one_food})
	best_foods = dict(sorted(my_dict.items(), key=lambda item: item[1]))

	values = Food.objects.all().filter(food__foodmenu__order_id__status = "Peyment").annotate(our_sum=Sum("food__foodmenu__number")).order_by("-our_sum")[:5]

	best_branchs = Branch.objects.filter(foods__food__foodmenu__order_id__status='Peyment').annotate(sums =Sum("foods__food__foodmenu__order_id__total_price") ).order_by("-sums")[:5]

	context = {'products':products,"way2":best_foods,"best_foods":values,"best_branchs":best_branchs,"branches":branches}
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
	template_name = "deletefoodpanel.html"
	success_url = reverse_lazy("paneladmin")
	fields = "__all__"

class DeleteItem(DeleteView):
	model = OrderItem
	template_name = "deletefood.html"
	success_url = reverse_lazy("cart")
	fields = "__all__"


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
			device = request.COOKIES['device']
			customer = request.user.email
			our_customer = Customer.objects.get(email = customer)

			our_customer.device = device
			our_customer.save
			customer = our_customer
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(username = device,email=device+"@gmail.com",device=device )
	
		if (Order.objects.filter(customer_id=customer).filter(status="Order")):
			# print(FoodMenu.objects.filter(foodmenu__order_id__status="Order").filter(foodmenu__order_id__customer_id=customer).values_list("branch_id__name").last()[0],"___",FoodMenu.objects.filter(id = pk).values_list("branch_id__name").last()[0])	
			if (FoodMenu.objects.filter(id = pk).values_list("branch_id__name").last())[0] == FoodMenu.objects.filter(foodmenu__order_id__status="Order").filter(foodmenu__order_id__customer_id=customer).values_list("branch_id__name").first()[0]:
				if ((FoodMenu.objects.all().filter(id = pk).values_list('number').last())[0]>= int(request.POST['number'])):
					flag = True
					order, created = Order.objects.get_or_create(customer_id=customer, status="Order")
					orderItem, created = OrderItem.objects.get_or_create(order_id=order, food_menu_id=product)
					orderItem.number =request.POST['number']
					orderItem.save()
					
					return redirect('cart')
				else:
						context = {'product':product, "food":food ,'msg':"we dont have enough"}
						return render(request, 'product.html', context)
			else:
				context = {'product':product, "food":food ,'msg':"First remove all the foods from other branches"}
				return render(request, 'product.html', context)
		else:
			print("hi")
			if ((FoodMenu.objects.all().filter(id = pk).values_list('number').last())[0]>= int(request.POST['number'])):
				order, created = Order.objects.get_or_create(customer_id=customer, status="Order")
				orderItem, created = OrderItem.objects.get_or_create(order_id=order, food_menu_id=product)
				orderItem.number =request.POST['number']
				orderItem.save()	
				return redirect('cart')
			else:
				context = {'product':product, "food":food ,'msg':"we dont have enough"}
				return render(request, 'product.html', context)
    			

	context = {'product':product, "food":food }
	return render(request, 'product.html', context)

def cart(request):# باید بعدا درست شه faz3
	if request.method == 'POST':
		if request.user.email :
			
			orderitems = OrderItem.objects.filter(order_id__status = "Order")
			if orderitems:
				one_of_foods_name = Food.objects.filter(food__foodmenu__order_id__customer_id__username = request.user.username).values_list("name" , flat=True)
				q1 = Q(foods__food__foodmenu__order_id__status="Order")
				q2 = Q(foods__name = one_of_foods_name)
				# branch = Branch.objects.get( q1 & q2 )
				total = sum([item.get_total for item in orderitems])
				order = Order.objects.get(status = "Order")
				order.total_price = total
				order.status = "Peyment"
				# order.branch = branch
				order.save()
				return render(request,"success.html")

			
	try:
		customer = request.user.device
		
		

	except:
		device = request.COOKIES['device']
		customer = device
		
		
	orderitems=OrderItem.objects.filter(order_id__customer_id__device=customer).filter(order_id__status = "Order")
	food = Food.objects.filter(food__foodmenu__order_id__customer_id__device=customer)
	orders = Order.objects.filter(customer_id__device=customer).filter(status = "Order")
	customer_address = CustomerAdress.objects.filter(customer__device=customer)
	print(customer_address)
	context = {'order':orders,"orderitems": orderitems,"food":food,"address":customer_address}

	return render(request, 'cart.html', context)



def search(req):
   
    results=[]
    if req.method == 'GET':
        query = req.GET.get('search')
        if query == '':
            query = 'None'
        results = FoodMenu.objects.filter(Q(food_id__name__icontains= query)| Q(branch_id__name__icontains=query))
    context ={'query': query, 'results': results}
    print(results)
    return render(req, 'search.html', context)


#panel Resturant



class BranchUpdate(UpdateView):
    model = Branch
    template_name = "restaurant/branch_edit.html"
    success_url = reverse_lazy('restaurant_panel')
    fields= "__all__"

class RestaurantCreate(CreateView):
    model = Branch
    template_name = "resturantPanel/branch_form.html"
    success_url = reverse_lazy('create_menu')
    fields = "__all__"

class MenuCreate(CreateView):
    model = FoodMenu
    template_name = "resturantPanel/create_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = "__all__"

def manager_menus(request):
	manager_menus = FoodMenu.objects.all().filter(branch_id__manager_id__username= request.user.username)
	return render(request,"resturantPanel/restaurantbranch.html",{"manager_menus":manager_menus})

class MenuUpdate(UpdateView):
    model = FoodMenu
    template_name = "resturantPanel/edit_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = "__all__"

class MenuDelete(DeleteView):
    model = FoodMenu
    template_name = "resturantPanel/delete_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = "__all__"