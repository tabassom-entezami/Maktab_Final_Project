
from django.db import models
from accounts.models import Manager,CustomerAdress

    

class Resturant(models.Model):
    name=models.CharField(max_length=30)
    class Meta:
        abstract = True
    

class Beranch(Resturant):
    OPEN_STATUS={
        (0,"Open"),
        (1,"Close"),
    }
    manager_id=models.OneToOneField(Manager,on_delete=models.CASCADE)
    category_id=models.OneToOneField("FoodCategory",on_delete=models.CASCADE)
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=30)
    discreption=models.TextField(max_length=200)
    is_open= models.BooleanField(choices=OPEN_STATUS, verbose_name='IsOpen', default=False)
    create_date=models.DateTimeField(auto_now_add=True)
    order_id=models.ForeignKey("Order",on_delete=models.CASCADE,null=True)

    def __str__(self) :
        return self.name

class Menu(models.Model):
    branch_id=models.OneToOneField(Beranch,on_delete=models.CASCADE)
    food_id=models.ManyToManyField("Food")
    price=models.IntegerField(null=False, blank=False)
    quantity=models.IntegerField(null=False, blank=False)

    def __str__(self) -> str:
        return f'{self.branch_id}'


class Food(models.Model):
    name=models.CharField(max_length=30)
    photo = models.ImageField(upload_to='image', null=True, blank=True, default=None)
    discreption=models.TextField(max_length=200)
    create_date=models.DateTimeField(auto_now_add=True)
    foodcategory_id=models.ForeignKey("FoodCategory",on_delete=models.CASCADE)
    

    def __str__(self) :
        return self.name

class FoodCategory(models.Model):
    type=models.CharField(max_length=30)

    def __str__(self) :
        return self.type

class Meal(models.Model):
    name=models.CharField(max_length=30)
    food_id=models.ManyToManyField(Food)

    def __str__(self) :
        return self.name

class Order(models.Model):
    ORDER_STATUS = (
        ('Order', 'Order'),
        ('Peyment', 'Peyment'),
        ('Send', 'Send'),
        ('Delivery', 'Delivery'),
        
    )
    order_count=models.IntegerField()
    total_price=models.IntegerField()
    delivery_time=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20, choices=ORDER_STATUS, default='Record')
    created_date=models.DateTimeField(auto_now_add=True)
    customeraddress_id=models.OneToOneField(CustomerAdress,on_delete=models.CASCADE)

    def __str__(self) :
        return self.status