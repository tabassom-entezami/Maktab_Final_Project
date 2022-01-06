from django.contrib import admin
from .models import *


from django.contrib import admin 
from .models import * 
 
 
@admin.register(Branch) 
class BranchAdmin(admin.ModelAdmin): 
    list_display = ['address','city', 'is_open'] 
    list_display_links =  ['city'] 
    search_fields = ['city'] 
    list_filter = ['city'] 
 
 
@admin.register(Food) 
class FoodAdmin(admin.ModelAdmin): 
    list_display = ['name','create_date'] 
    list_display_links =  ['name'] 
    search_fields = ['name'] 
    list_filter = ['name'] 
 
 
 
   
     
@admin.register(Category) 
class FoodCategoryAdmin(admin.ModelAdmin): 
    field_list=['type'] 
    search_fields = ['type'] 
   
@admin.register(Meal) 
class MealAdmin(admin.ModelAdmin): 
    field_list=['name','food_id'] 
    search_fields = ['name']  
    list_filter = ['name']   
 
@admin.register(Order) 
class OrderAdmin(admin.ModelAdmin): 
    field_list=['status','total_price'] 
    search_fields = ['status','created_date']  
    list_filter = ['status'] 
     
    
 
@admin.register(FoodMenu) 
class FoodMenuAdmin(admin.ModelAdmin): 
    list_display = ['price','number'] 
    # list_display_links =  ['food_id'] 
    search_fields = ['food_id','price'] 
     
 
 
@admin.register(OrderItem) 
class OrderItemAdmin(admin.ModelAdmin): 
    list_display = ['order_id','number'] 
    list_display_links =  ['order_id'] 
    search_fields=['order_id']