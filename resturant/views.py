from django.db import models
from django.db.models import fields
from django.db.models.expressions import OrderBy
from django.db.models.aggregates import Count, Sum
from django.db.models import Q
from django.forms.widgets import NumberInput
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView,CreateView,UpdateView
from resturant.forms import *
from .models import *
from accounts.models import *
from .decorators import *
from django.views.generic import ListView
from accounts.models import *
from django.contrib.auth.decorators import login_required 
from django.db.models import Count 
from django.http import JsonResponse, request
from rest_framework.response import Response
from .serializer import *
from django.urls import reverse_lazy , reverse
from .serializer import *

#home
def home_page(re):
	products = FoodMenu.objects.all().filter(number__gt=0)
	foods_deliverd= Food.objects.all().exclude(food__foodmenu__order_id__status = "Order")
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

	# if re.method == 'POST'  and re.is_ajax():
	# 	text = re.POST.get('search_input')
	# 	if text :
	# 		branch = Branch.objects.filter(name__icontains=text)
	# 		food = Food.objects.filter(name__icontains=text)
	# 		branches ={}
	# 		foods ={}
	# 		if branch:
	# 			serializer_branch = BranchSerializer(branch,many=True,context={'request': request})
	# 			branches = serializer_branch.data    
			
	# 		if food:
	# 			serializer_food = FoodSerializer(food,many=True,context={'request': request})
	# 			foods = serializer_food.data
			
	# 		return Response({"branches":branches , "foods":foods})
	# 	else:
	# 		Response({"branches":[] , "foods":[],"msg":"does not match"})

				
					
	return render(re, "Home.html" , context)



@login_required
def panel_admin(req):
	foods = Food.objects.all()
	content = {"foods": foods}
	return render(req,"paneladmin.html",content)

# سرچ 
def search(re):
	results=[]
	if re.method == "GET":
		
		query = re.GET.get('search')
		if query == '':
			query = 'None'
		results = FoodMenu.objects.filter(Q(food_id__name__icontains= query)| Q(branch_id__name__icontains=query ))

	context ={'query': query, 'results': results}
	
	return render(re, 'search.html', context)



# def sample_django_template(req):
# 	if req.method == 'POST'  and req.is_ajax():
# 		print("_________________________-")
# 		text = req.POST.get('text')
		
# 		p = FoodMenu.objects.filter(Q(food_id__name__icontains= text)| Q(branch_id__name__icontains=text ))
# 		if p in p:
# 			return JsonResponse({
# 				'food':p.values_list('name', flat=True),
# 				'price': p.price,
# 				"number":p.number,
# 				'food_id': (p.food_id.name),
# 				"branch_id":(p.branch_id.name),

# 			})
# 		else:
# 			return JsonResponse({
# 				'food': [],
# 				'msg' : "doesn't match any files",
# 			})

# 	return render(req,'search.html',{
# 		'test' : "test"
# 	})



# def main_view(request):
#       return render(request, 'search.html',{})

# def food_detail_view(request,pk):
#     obj = Food.objects.get(id = pk)
#     return render(request,"search.html",{"results":obj})

# def search2(request):
#     if request.is_ajax() :
        
#         game = request.POST.get('search')
#         qs = FoodMenu.objects.filter(Q(food_id__name__icontains= search)| Q(branch_id__name__icontains=search ))
#         return render(request,"search.html",{'data':game,'qs':qs})
#     res = None
#     return render({res:"nothing found"})


# admin
@superuser_required()
class AddFoodPanelAdmin(CreateView):
	model = Food
	success_url = reverse_lazy("paneladmin")
	template_name = "addfood.html"
	fields = "__all__"

@superuser_required()
class AddCategoryPanelAdmin(CreateView):
	model = Category
	success_url = reverse_lazy("paneladmin")
	template_name = "addcategory.html"
	fields = "__all__"

@superuser_required()
class UpdateFoodPanelAdmin(UpdateView):
	model = Food
	success_url = reverse_lazy("paneladmin")
	template_name = "updatefood.html"
	fields = "__all__"

@superuser_required()
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


def resturant(re):
	products = FoodMenu.objects.all()
	food = Food.objects.all()
	context = {'products':products,"food":food}
	if re.method == 'POST'  and re.is_ajax():
		text = re.POST.get('search_input')
		if text :
			branch = Branch.objects.filter(name__icontains=text)
			food = Food.objects.filter(name__icontains=text)
			branches ={}
			foods ={}
			if branch:
				serializer_branch = BranchSerializer(branch,many=True,context={'request': request})
				branches = serializer_branch.data    
			
			if food:
				serializer_food = FoodSerializer(food,many=True,context={'request': request})
				foods = serializer_food.data
			
			return Response({"branches":branches , "foods":foods})
		else:
			Response({"branches":[] , "foods":[],"msg":"does not match"})

	return render(re, 'resturant.html', context)

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
			if Customer.objects.get(username = device):
				have_to_delete = Customer.objects.get(username = device)
				have_to_delete.delete()
			our_customer.device = device
			our_customer.save()
			customer = our_customer
			
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(username = device,email=device+"@gmail.com",device=device )
	


		if (Order.objects.filter(customer_id=customer).filter(status="Order") and FoodMenu.objects.filter(foodmenu__order_id__status="Order").filter(foodmenu__order_id__customer_id=customer)):
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
				device = request.COOKIES['device']
				adres = request.POST["customer_address"]
				customer_addres = CustomerAdress.objects.get(id = adres)
				branch_id = FoodMenu.objects.filter(foodmenu__order_id__status="Order").filter(foodmenu__order_id__customer_id__device=device).values_list("branch_id__id").first()[0]
				branch = Branch.objects.get(id = branch_id )
				total = sum([item.get_total for item in orderitems])
				order = Order.objects.get(status = "Order")
				order.total_price = total
				order.status = "Peyment"
				order.branch = branch
				order.customeraddress_id = customer_addres
				order.save()
				return render(request,"success.html")
			
			
	try:
		customer = request.user
		device = request.COOKIES['device']
		if Customer.objects.get(username = request.user.device):
			have_to_delete = Customer.objects.get(username = request.user.device)
			have_to_delete.delete()
		our_customer = Customer.objects.get(email = customer.email)
		our_customer.device = device
		our_customer.save()
		customer = our_customer
		
	except:
		device = request.COOKIES['device']
		customer = device
		
		
	orderitems=OrderItem.objects.filter(order_id__customer_id__device=customer).filter(order_id__status = "Order")
	food = Food.objects.filter(food__foodmenu__order_id__customer_id__device=customer)
	orders = Order.objects.filter(customer_id__device=customer).filter(status = "Order")
	customer_address = CustomerAdress.objects.filter(customer__username = request.user.username)
	print(customer_address)
	context = {'order':orders,"orderitems": orderitems,"food":food,"address":customer_address}

	return render(request, 'cart.html', context)








#panel Resturant
@is_staff_required()
class BranchUpdate(UpdateView):
    model = Branch
    template_name = "restaurant/branch_edit.html"
    success_url = reverse_lazy('restaurant_panel')
    fields= "__all__"
# @is_staff_required()
# class RestaurantCreate(CreateView):
#     model = Branch
#     template_name = "resturantPanel/branch_form.html"
#     success_url = reverse_lazy('create_menu')
#     fields = "__all__"

@is_staff_required()
class MenuCreate(CreateView):
	model = FoodMenu
	template_name = "resturantPanel/create_menu.html"
	success_url = reverse_lazy('restaurant_panel')
	fields =["food_id","number","price"]

	def post(self, request, *args, **kwargs):
		branch_id = Branch.objects.get(manager_id__username = self.request.user.username)
		food_id = request.POST["food_id"]
		food = Food.objects.get(id = food_id)
		price = request.POST["price"]
		number = request.POST["number"]
		form = self.get_form()
		print(form)
		if form.is_valid():

			new =FoodMenu.objects.create(branch_id = branch_id,food_id = food , price = price ,number = number )
			return redirect("restaurant_panel")
		else:
			return self.form_invalid(form)

	
    		
# @login_required
# def manager_menus(request):
# 	manager_menus = FoodMenu.objects.all().filter(branch_id__manager_id__username= request.user.username)
# 	branch = Branch.objects.get(manager_id__username = request.user.username)
# 	manager = Manager.objects.get(username = request.user.username)
# 	orders = Order.objects.filter(branch__manager_id__username = request.user.username).exclude(status = "Order")
# 	return render(request,"resturantPanel/restaurantbranch.html",{"manager_menus":manager_menus , "branches" : branch , "manager":manager ,"orders":orders})

@is_staff_required()
class ManagerMenus(TemplateView):
	template_name = "resturantPanel/restaurantbranch.html"
	def get_context_data(self, **kwargs) :
		context = super().get_context_data(**kwargs)
		context["manager_menus"]=FoodMenu.objects.all().filter(branch_id__manager_id__username= self.request.user.username)
		context["branches"] = Branch.objects.get(manager_id__username = self.request.user.username)
		context["manager"] = Manager.objects.get(username = self.request.user.username)
		context["orders"] = Order.objects.filter(branch__manager_id__username = self.request.user.username).exclude(status = "Order")
		return context


@is_staff_required()
class MenuUpdate(UpdateView):
    model = FoodMenu
    template_name = "resturantPanel/edit_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = ["number","price"]

@is_staff_required()
class MenuDelete(DeleteView):
    model = FoodMenu
    template_name = "resturantPanel/delete_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = "__all__"


class Branches(DetailView):
	model = Branch
	template_name = "branch_detail.html"
	fields ="__all__"
@is_staff_required()
class BranchEdit(UpdateView):
	model = Branch
	template_name = "resturantPanel/branch_edit.html"
	success_url = reverse_lazy('restaurant_panel')
	fields = ["name","category_id","address","city","discreption","is_open"]
@is_staff_required()
class ManagerEdit(UpdateView):
	model = Manager
	template_name = "resturantPanel/manager_edit.html"
	success_url = reverse_lazy('restaurant_panel')
	fields = ["first_name","last_name","username","password"]
	

@customer_required()
class CustomerPanel(TemplateView):
	template_name = "customerPanel/customer_panel.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["orders"] = Order.objects.filter(customer_id__username = self.request.user.username)
		context["address"] = Address.objects.filter(customer_address__customer__username = self.request.user.username)
		return context

@customer_required()
class CustomerEdit(UpdateView):
	model = Customer
	template_name = "customerPanel/customer_edit.html"
	fields = ["first_name","last_name","username","password"]
	success_url = reverse_lazy('customer_panel')
