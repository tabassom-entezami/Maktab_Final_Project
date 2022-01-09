from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    email=models.EmailField(unique=True)
    


class Customer(CustomUser):
    
    address=models.ManyToManyField("Address",through="CustomerAdress",related_name='address')
    device = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name="customer"

    # def save(self,*args, **kwargs):
    #     if not self.id:
    #         self.is_staff = False
    #         self.is_superuser = False
    #     return super(Manager,self).save(*args,**kwargs)




class CustomerAdress(models.Model):

    default = models.BooleanField()
    customer=models.ForeignKey("Customer",on_delete=models.SET_NULL,null=True,related_name='customer1')
    address = models.ForeignKey("Address",on_delete=models.SET_NULL,null=True,related_name="customer_address")

    class Meta:
        ordering = ['pk']
        verbose_name="customerAddress"
    

    @staticmethod
    def has_default(customer):
        for address in CustomerAdress.objects.filter(customer=customer):
            if address.default is True:
                return True
        return False

class Address(models.Model):
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    plaque = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['pk']

    def __str__(self) -> str:
        return self.city + self.street + self.plaque

class Manager(CustomUser):
    class Meta:
        # proxy=True
        verbose_name="resturant manager"

    def save(self,*args, **kwargs):
        if not self.id:
            self.is_staff = True
            self.is_superuser = False
        return super(Manager,self).save(*args,**kwargs)
     
    

class Admin(CustomUser):
    class Meta:
        proxy=True
        verbose_name="superuser"
        
    def save(self,*args, **kwargs):
        if not self.id:
            # self.is_staff = True
            self.is_superuser = True
        return super(Admin,self).save(*args,**kwargs)

    


 