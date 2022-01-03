from rest_framework import serializers
from accounts.models import Customer
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email']
        

class FoodSerilizer(serializers.ModelSerializer):
    # owner = CustomerSerializer(read_only=True)
    class Meta:
        model = Food
        fields = "all"

class FoodCategorySerilizer(serializers.ModelSerializer):
    # owner = CustomerSerializer(read_only=True)
    class Meta:
        model = Category
        fields = "all"

class MealCategorySerilizer(serializers.ModelSerializer):
    # owner = CustomerSerializer(read_only=True)
    class Meta:
        model = Meal
        fields = "all"


class RestaurantBranchSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "all"