from django.contrib import admin
from .models import *


admin.site.register(Branch)
admin.site.register(Menu)
admin.site.register(Food)
admin.site.register(Category)
admin.site.register(Meal)
admin.site.register(Order)
# admin.site.register(Resturant)
admin.site.register(FoodMenu)
admin.site.register(OrderItem)

# Register your models here.
