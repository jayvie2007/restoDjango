from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from jresto.models import CustomAdmin, CustomerDetails
from jresto.serializers.authentication_serializers import CustomerGetSerializer, AdminGetSerializer, AdminLoginSerializer
from jresto import utils

from constants.status_code import *



class GetAdminApi(APIView):
    def get(self, request):
        admins = CustomAdmin.objects.all()
        serializers = AdminGetSerializer(admins, many=True)
        return Response({"List of Admins": serializers.data})
    
class GetCustomerApi(APIView):
    def get(self, request):
        customers = CustomerDetails.objects.all()
        serializers = CustomerGetSerializer(customers, many=True)
        return Response({"List of Customer": serializers.data})


