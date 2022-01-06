from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', ]

admin.site.register(CustomUser,CustomUserAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email' , "username"]
    list_display_links = ['email',"username"]
    search_fields = ['email']
    
    def get_queryset(self, request):
            return Customer.objects.filter(is_staff=False)


@admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
    list_display = ['city', 'street', 'plaque']
    search_fields = ['city']
    empty_value_display = "---"

@admin.register(CustomerAdress)
class CustomerAdressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'address', 'default']
    list_display_links = ['address']
    empty_value_display = "---"

    def save_model(self, request, obj, form, change) -> None:
        
        obj.set_password(form.cleaned_data["password"])
        obj.save
@admin.register(Manager)
class managerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['email']
    empty_value_display = "---"

    
    def get_queryset(self, request):
        return Manager.objects.filter(is_staff=True, is_superuser=False)

    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()

@admin.register(Admin)
class AdminProxyAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
    list_display_links = ['username']
    list_editable = ['email']
    search_fields = ['username', 'email']
    empty_value_display = "---"
    
    def get_queryset(self, request):
        return Admin.objects.filter(is_superuser=True)

# Register your models here.
