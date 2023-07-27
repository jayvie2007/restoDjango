from django.shortcuts import render

from rest_framework.response import Response

from jresto.models import CustomAdmin
from jresto.serializers.authentication_serializers import AdminGetSerializer, AdminLoginSerializer
from jresto import utils

from constants.status_code import *

def get_admin(request):
    admins = CustomAdmin.objects.all()
    serializers = AdminGetSerializer(admins, many=True)
    return Response({"List of Admins": serializers.data})
