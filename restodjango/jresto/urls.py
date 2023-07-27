from django.urls import path, include

from .views import views_api_authentication 
from .views import views_api_templates
from .views import views_authentication 
from .views import views_templates 
 

###### API_AUTHENTICATION ######
urlpatterns = [
    path('api/authentication', views_api_authentication.get_admin, name="dashboard"),
]

###### API_TEMPLATES ######
urlpatterns += [
    path('api/product/food', views_api_templates.menu_get_food.as_view(), name="get_food"),
    path('api/product/addfood', views_api_templates.menu_add_food.as_view(), name="add_food"),
    path('api/product/editfood', views_api_templates.menu_edit_food.as_view(), name="edit_food"),
    path('api/product/deletefood', views_api_templates.menu_delete_food.as_view(), name="delete_food"),
    
    path('api/product/drink', views_api_templates.menu_get_drink.as_view(), name="get_drink"),
    path('api/product/adddrink', views_api_templates.menu_add_drink.as_view(), name="add_drink"),
    path('api/product/editdrink', views_api_templates.menu_edit_drink.as_view(), name="edit_drink"),
    path('api/product/deletedrink', views_api_templates.menu_delete_drink.as_view(), name="delete_drink"),
    
    path('api/product/side', views_api_templates.menu_get_side.as_view(), name="get_side"),
    path('api/product/addside', views_api_templates.menu_add_side.as_view(), name="add_side"),
    path('api/product/editside', views_api_templates.menu_edit_side.as_view(), name="edit_side"),
    path('api/product/deleteside', views_api_templates.menu_delete_side.as_view(), name="delete_side"),
]

###### AUTHENTICATION ######
urlpatterns += [
    path('admin/register', views_authentication.register, name="admin_registeer"),
]

###### TEMPLATES ######
urlpatterns += [
    path('', views_templates.index, name="index"),
]
