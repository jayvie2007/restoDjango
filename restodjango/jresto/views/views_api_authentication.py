from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from jresto.models import CustomUser
from jresto.serializers.authentication_serializers import CustomerGetSerializer, AdminGetSerializer, AdminLoginSerializer
from jresto import utils

from constants.status_code import *


class GetAdminApi(APIView):
    def get(self, request):
        customers = CustomUser.objects.filter(user_level='Admin')
        serializers = AdminGetSerializer(customers, many=True)
        return Response({"List of Admin": serializers.data})

class GetCustomerApi(APIView):
    def get(self, request):
        customers = CustomUser.objects.filter(user_level='Customer')
        serializers = CustomerGetSerializer(customers, many=True)
        return Response({"List of Customer": serializers.data})


