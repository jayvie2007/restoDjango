from django.urls import path, include

from .views import views_api_authentication, views_api_templates, views_templates 
 
###### API_AUTHENTICATION ######
urlpatterns = [
    path('api/authentication/admin', views_api_authentication.GetAdminApi.as_view(), name="adminAPI"),
    path('api/authentication/customer', views_api_authentication.GetCustomerApi.as_view(), name="customerAPI"),
]

###### API_TEMPLATES ######
urlpatterns += [
    path('api/product/', views_api_templates.GetProductAPIView.as_view(), name="get_product"),
    path('api/product/add', views_api_templates.PostProductAPIView.as_view(), name="add_product"),
    path('api/product/edit/<str:product_id>', views_api_templates.PutProductAPIView.as_view(), name="edit_product"),
    path('api/product/delete/<str:product_id>', views_api_templates.DeleteProductAPIView.as_view(), name="delete_product"),
   
    path('api/customer/feedback', views_api_templates.GetCustomerFeedback.as_view(), name="get_feedback"),
]

###### AUTHENTICATION ######
urlpatterns += [
    path('jresto/edit/<str:uid>', views_templates.edit_customer, name="user_edit"),
    path('jresto/register', views_templates.register_customer, name="user_register"),
    path('jresto/login', views_templates.login_customer, name="user_login"),
    path('jresto/logout', views_templates.logout_customer, name="user_logout"),
]

###### TEMPLATES ######
urlpatterns += [
    path('', views_templates.index, name="index"),

    path('jresto/menu', views_templates.menu, name="menu"),
    path('jresto/menu/food', views_templates.food, name="menu_food"),
    path('jresto/menu/drink', views_templates.drink, name="menu_drink"),
    path('jresto/menu/side', views_templates.side, name="menu_side"),

    path('jresto/contact-us', views_templates.contact, name="contact_us"),
]

###### ADMIN ######
urlpatterns += [
    path('jresto/admin/menu', views_templates.admin_menu, name="admin_menu"),
    path('jresto/admin/product/', views_templates.admin_display_menu, name="menu_product"),
    path('jresto/admin/product/add', views_templates.admin_add_menu, name="menu_product_add"),
    path('jresto/admin/edit/product/<str:product_id>', views_templates.admin_edit_menu, name="menu_product_edit"),
    path('jresto/admin/delete/product/<str:product_id>', views_templates.admin_delete_menu, name="menu_product_delete"),
    path('jresto/admin/delete/feedback/<str:id>', views_templates.admin_feedback_delete, name="admin_feedback_delete"),
    path('jresto/admin/feedback', views_templates.admin_feedback, name="admin_feedback"),
]

