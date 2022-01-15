from os import name
from django.urls import path

from accounts.views import *
from .views import *

urlpatterns = [

    path('', home_page, name="Home"),
    path('foods/',resturant, name="store"),
	path('cart/', cart, name="cart"),
	path('product/<int:pk>/', product, name="product"),
    path('deleteitem/<int:pk>/',DeleteItem.as_view(),name ="deleteitem"),
    path('foodadd/', AddFoodPanelAdmin.as_view() , name = "addfood"),
    path('foodupdate/<int:pk>/', UpdateFoodPanelAdmin.as_view() , name = "updatefood"),
    path('fooddelete/<int:pk>/', DeleteFoodPanelAdmin.as_view() , name = "deletefood"),
    path('panel/', panel_admin , name ="paneladmin"),
    path('categoryadd/', AddCategoryPanelAdmin.as_view() , name = "addcategory"),
    path("branch/<int:pk>/",Branches.as_view() , name = "branches" ),
    path("statusupdate/<int:pk>/", MenuUpdate.as_view() , name ="statusupdate"),
    
    path("search/" , search , name="search"),
    path("search2/", search_result ,name = "search2"),
    path("<int:pk>/",get_info_search ,name="get_search") ,
   
    
    #پنل رستوران
    path("manager/edit/<int:pk>/" , ManagerEdit.as_view(),name = "manager_edit"),
    path('branch/edit/<int:pk>/',BranchEdit.as_view(),name="branch_edit"),
    path('restaurant_panel/',ManagerMenus.as_view(),name="restaurant_panel"),
    path("create_menu/",MenuCreate.as_view(),name="create_menu"),
    path("delete_menu/<int:pk>/",MenuDelete.as_view(),name="delete_menu"),
    path("edit_menu/<int:pk>/",MenuUpdate.as_view(),name="edit_menu"),

    #پنل مشتری
    path("yourPanel/",CustomerPanel.as_view(),name="customer_panel")  
    
]
