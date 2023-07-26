from django.urls import path, include

from . import views_api

urlpatterns = [
    path('', views_api.index, name="dashboard")
]
