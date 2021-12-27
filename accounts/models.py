from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    


class Customer(CustomUser):
    customeraddress_id=models.ManyToManyField("CustomerAdress",related_name='customer_address')
    class Meta:
        verbose_name="customer"
    

class CustomerAdress(models.Model):
    city = models.CharField(max_length=10)
    street = models.CharField(max_length=10)
    plaque = models.CharField(max_length=10)



class Manager(CustomUser):
    class Meta:
        proxy=True
        verbose_name="resturant manager"

class Admin(CustomUser):
    class Meta:
        proxy=True
        verbose_name="superuser"
        verbose_name_plural = 'superusers'


 