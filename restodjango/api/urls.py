from django.urls import path, include

from . import views

urlpatterns = [
    path('food/', views.FoodGetApi.as_view(), name="get_food"),
    #path('food/add', views.FoodGetApi.as_view(), name="add_food")
]
