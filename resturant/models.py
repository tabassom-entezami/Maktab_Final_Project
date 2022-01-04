
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL , PROTECT
from accounts.models import Manager,CustomerAdress
# from multiselectfield import MultiSelectField
from accounts.models import *
import jdatetime
from django.core.validators import MinValueValidator
    

class Resturant(models.Model):
    name=models.CharField(max_length=30)
    class Meta:
        abstract = True
            

class Branch(Resturant):
    OPEN_STATUS={
        (0,"Open"),
        (1,"Close"),
    }
    # branch_name = models.CharField(max_length=100)
    manager_id=models.OneToOneField(Manager,on_delete=models.PROTECT,verbose_name="which_manager",related_name='maneger')
    # چون که بدون منیجر نمیتونیم داشته باشیم
    # category_id=models.ManyToManyRel("FoodCategory",on_delete=models.CASCADE,verbose_name="which_category",related_name="category_id")
    category_id=models.ForeignKey("Category",on_delete=models.PROTECT,related_name="category_branch")
    #چون که برنچ بدون کتگوری نباید داشته باشیم
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=30)
    discreption=models.TextField(max_length=200)
    is_open= models.BooleanField(choices=OPEN_STATUS, verbose_name='IsOpen', default=False)
    create_date=models.DateTimeField(auto_now_add=True)
    # order_id=models.ForeignKey("Order",on_delete=models.CASCADE,null=True,verbose_name="which_order",related_name='order_id')
    # resturant_id = models.ForeignKey("resturant",on_delete=models.SET_NULL,null=True,related_name ="resturant",verbose_name="which_resturant")
    # هیچ رستورانی بدون شعبه و یا برعکس نمیتونه باشه

    @property
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_date)

    def __str__(self) :
        return f"{self.name} "

# class Menu(models.Model):
#     branch_id=models.OneToOneField(Branch,on_delete=models.CASCADE,related_name="branch")
#     #اگه برنچ پاک شه منوش هم که مختص به خودشه پاک میشه
#     # foodmenu_id=models.ManyToManyField("FoodMenu",related_name='foodmenu_id')
#     # price=models.IntegerField(null=False, blank=False)
#     # quantity=models.IntegerField(null=False, blank=False)

#     def __str__(self) -> str:
#         return f'{self.branch_id}'


class Food(models.Model):
    name=models.CharField(max_length=30)
    photo = models.ImageField(upload_to='image', null=True, blank=True, default=None)
    discreption=models.TextField(max_length=200)
    create_date=models.DateTimeField(auto_now_add=True)
    foodcategory_id=models.ForeignKey("Category",on_delete=models.PROTECT,related_name="food_category")
    # کتگوری نداریم پس نباید پاک شن غذای بدون 
    # menu_id = models.ManyToManyField('Menu',through="FoodMenu",related_name='food_menu')
    meal_id = models.ManyToManyField("Meal",related_name="meal")
    branch_id = models.ManyToManyField(Branch,through='FoodMenu',related_name='food_menu')

    @property
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.create_date)
    def __str__(self) :
        return self.name

class FoodMenu(models.Model):
    food_id = models.ForeignKey("Food", on_delete=models.PROTECT ,related_name="food")
    # که غذا تا زمانی که توی منویی هست نشه پاک شه
    # menu_id = models.ForeignKey("Menu",on_delete=models.CASCADE,related_name="menu")
    branch_id = models.ForeignKey("Branch",on_delete=models.CASCADE,related_name="branch_id")
    #ه قود پاک شه حتما باید منوش هم بره
    price = models.IntegerField()
    number = models.IntegerField(validators = [MinValueValidator(1)])
    


    def __str__(self) :
        return f"""{self.food_id} , {self.branch_id} """

class OrderItem(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE ,related_name='order')
    #اگه اوردر ایتم حذف شه اوردر هم حذف میشه
    food_menu_id = models.ForeignKey(FoodMenu, on_delete=models.SET_NULL,null=True, related_name='foodmenu')
    #اگه فود منو
    number = models.IntegerField(null=True,validators = [MinValueValidator(1)])
    # total_price = models.IntegerField()

    @property #بعدا درست شه
    def get_total(self):
        foodname = str(Food.objects.all().filter(food__foodmenu__id = self.id).values_list("name")[0][0])
        print(foodname)
        total = ( (self.number) * int(FoodMenu.objects.all().filter(foodmenu__order_id = self.order_id ).filter(foodmenu__order_id__isnull=False).filter(food_id__name = foodname).values_list('price')[0][0]))
        return total

    
    def __str__(self):
        return f"{self.order_id} order"
class Category(models.Model):
    type=models.CharField(max_length=30)

    def __str__(self) :
        return self.type

class Meal(models.Model):
    # MEAL_CHOICES=(
    #     ('dinner','dinner'),
    #     ("breakfast",'breakfast'),
    #     ("lunch","lunch")

    # )
    name=models.CharField(max_length=30)
    # food_id=models.ManyToManyField(Food,related_name='food_meal')
    # name = models.MultipleChoiceField(choices = MEAL_CHOICES)
    # food_id=models.ManyToManyField(Food,related_name='food_meal')

    def __str__(self) :
        return self.name

class Order(models.Model):
    ORDER_STATUS = (
        ('Order', 'Order'),
        ('Peyment', 'Peyment'),
        ('Send', 'Send'),
        ('Delivery', 'Delivery'),
        
    )
    # order_count=models.IntegerField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE,  blank=True)
    # food_menu_id = models.ManyToManyField(FoodMenu)
    total_price=models.IntegerField( null=True)
    delivery_time=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=8, choices=ORDER_STATUS, default='Order')
    created_date=models.DateTimeField(auto_now_add=True)
    customeraddress_id=models.ForeignKey(CustomerAdress,on_delete=models.CASCADE,null=True,related_name="custumer_address")
    # order_item_id = models.ManyToManyField(OrderItem, verbose_name="order_item",related_name="order_item_id")
    foodmenu_id=models.ManyToManyField(FoodMenu,through=OrderItem,related_name='food')
    branch = models.ForeignKey('Branch',on_delete=models.SET_NULL,null=True,related_name="delivery")
    #بدون برنچ اردر نمیخوایم
    
    @property
    def get_cart_total(self): #بعدا اوکی شه
        orderitems = OrderItem.objects.filter(order_id = self.id)
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = OrderItem.objects.filter(order_id = self.id)
        total = sum([item.number for item in orderitems])
        return total 




    @property
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_date)
    
     

    def __str__(self) :
        return self.status