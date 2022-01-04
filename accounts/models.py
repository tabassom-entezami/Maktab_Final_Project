from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    email=models.EmailField(unique=True)
    


class Customer(CustomUser):
    
    customeraddress_id=models.ManyToManyField("CustomerAdress",related_name='customer_address')
    device = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name="customer"

    # def save(self,*args, **kwargs):
    #     if not self.id:
    #         self.is_staff = False
    #         self.is_superuser = False
    #     return super(Manager,self).save(*args,**kwargs)
    

class CustomerAdress(models.Model):
    class Meta:
        ordering = ['pk']
            

    city = models.CharField(max_length=10)
    street = models.CharField(max_length=10)
    plaque = models.CharField(max_length=10)

    @staticmethod
    def has_default(customer):
        for address in CustomerAdress.objects.filter(customer_id=customer):
            if address.default is True:
                return True
        return False

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

    


 