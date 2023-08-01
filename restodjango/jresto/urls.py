from django.urls import path, include

from .views import views_api_authentication, views_api_templates, views_authentication, views_templates 
 
###### API_AUTHENTICATION ######
urlpatterns = [
    path('api/authentication/admin', views_api_authentication.GetAdminApi.as_view(), name="dashboard"),
    path('api/authentication/customer', views_api_authentication.GetCustomerApi.as_view(), name="dashboard"),
]

###### API_TEMPLATES ######
urlpatterns += [
    path('api/product/food', views_api_templates.GetFoodAPIView.as_view(), name="get_food"),
    path('api/product/addfood', views_api_templates.PostFoodAPIView.as_view(), name="add_food"),
    path('api/product/food/<str:product_id>', views_api_templates.PutFoodAPIView.as_view(), name="edit_food"),
    path('api/product/food/delete/<str:product_id>', views_api_templates.DeleteFoodAPIView.as_view(), name="delete_food"),
    
    path('api/product/drink', views_api_templates.GetDrinkAPIView.as_view(), name="get_drink"),
    path('api/product/adddrink', views_api_templates.PostDrinkAPIView.as_view(), name="add_drink"),
    path('api/product/drink/<str:product_id>', views_api_templates.PutDrinkAPIView.as_view(), name="edit_drink"),
    path('api/product/drink/delete/<str:product_id>', views_api_templates.DeleteDrinkAPIView.as_view(), name="delete_drink"),
    
    path('api/product/side', views_api_templates.GetSideAPIView.as_view(), name="get_side"),
    path('api/product/addside', views_api_templates.PostSideAPIView.as_view(), name="add_side"),
    path('api/product/side/<str:product_id>', views_api_templates.PutSideAPIView.as_view(), name="edit_side"),
    path('api/product/side/delete/<str:product_id>', views_api_templates.DeleteSideAPIView.as_view(), name="delete_side"),
   
    path('api/customer/feedback', views_api_templates.GetCustomerFeedback.as_view(), name="get_feedback"),
]

###### AUTHENTICATION ######
urlpatterns += [
    path('staff/register', views_authentication.register, name="admin_register"),
    path('staff/login', views_authentication.login, name="admin_login"),

    path('jresto/register', views_templates.register, name="customer_register"),
    path('jresto/login', views_templates.login, name="customer_login"),
]

###### TEMPLATES ######
urlpatterns += [
    path('', views_templates.index, name="index"),

    path('jresto/menu/food', views_templates.food, name="menu_food"),
    path('jresto/menu/drink', views_templates.drink, name="menu_drink"),
    path('jresto/menu/side', views_templates.side, name="menu_side"),

    path('jresto/contact-us', views_templates.contact, name="contact_us"),
]

