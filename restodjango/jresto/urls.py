from django.urls import path, include

from .views import views_api_authentication 
from .views import views_api_templates
from .views import views_authentication 
from .views import views_templates 
 

###### API_AUTHENTICATION ######
urlpatterns = [
    path('api/authentication', views_api_authentication.menu_add_drink, name="dashboard"),
]

###### API_TEMPLATES ######
urlpatterns += [
    path('api/product/food', views_api_templates.menu_add_drink, name="dashboard"),
]

###### AUTHENTICATION ######
urlpatterns += [
    path('admin/register', views_authentication.menu_add_drink, name="admin_registeer"),
]

###### TEMPLATES ######
urlpatterns += [
    path('', views_templates.index, name="index"),
]
