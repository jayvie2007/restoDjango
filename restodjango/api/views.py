from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from constants.status_code import * 

from jresto.models import Food, Drink, Side

from .serializers import FoodDetailsSerializer, DrinkDetailsSerializer, SideDetailsSerializer

import uuid

class FoodGetApi(APIView):
    def get(self, request):
        food = Food.objects.all()
        serializers = FoodDetailsSerializer(food, many=True)
        return Response({"Food List":serializers.data})
    
    def post(self, request):
        errors = {  }
        required_fields = ['name', 'description', 'price']

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field]= field_required_error
            if len(errors) != 0:
                return Response(data={'status':bad_request, 'message':errors}, status=bad_request)
                    
        nameInput = request.data['name']

        if 'name' in request.data and Food.objects.filter(name = nameInput).count() != 0:
            errors['name']=(f"The product {nameInput} is already in the list!")
        if len(errors) != 0:
                return Response(data={'status':bad_request, 'message':errors}, status=bad_request)
    
        uid = uuid.uuid4().hex[-8:]
        request.data._mutable=True
        request.data['uid'] = uid
        request.data._mutable=False
        serializers = FoodDetailsSerializer(data=request.data)
        print(uid)
        if serializers.is_valid():
            #serializers.save()
            return Response(data={"status": created, "message": product_added, "Food List":serializers.data})
        return Response(serializers.errors, status=bad_request)
    
class FoodEditApi(APIView):


    def put(self, request, product_id):
        try:
            foods = Food.objects.get(product_id = product_id)
        except Food.DoesNotExist:
                return Response(data={'status': not_found})
        
        serializers = FoodDetailsSerializer(foods, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data={'status':ok, 'message':updated})
        return Response(serializers.errors, status=bad_request)

class DrinkGetApi(APIView):
    def get(self, request):
        drink = Drink.objects.all()
        serializers = DrinkDetailsSerializer(drink, many=True)
        return Response({"Drink List":serializers.data})
    
    def post(self, request):
        errors = []
        required_fields = ['name', 'description', 'price']

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field]= field_required_error
            if len(errors) != 0:
                return Response(data={'status':bad_request, 'message':errors}, status=bad_request)
                    
        nameInput = request.data['name']

        if 'name' in request.data and Drink.objects.filter(name = nameInput).count() != 0:
            errors['name']=(f"The product {nameInput} is already in the list!")
        if len(errors) != 0:
                return Response(data={'status':bad_request, 'message':errors}, status=bad_request)
    
        uid = uuid.uuid4().hex[-8:]
        request.data._mutable=True
        request.data['uid'] = uid
        request.data._mutable=False
        serializers = DrinkDetailsSerializer(data=request.data)
        print(uid)
        if serializers.is_valid():
            #serializers.save()
            return Response(data={"status": created, "message": product_added, "Food List":serializers.data})
        return Response(serializers.errors, status=bad_request)

class SideGetApi(APIView):
    def get(self, request):
        side = Sidedish.objects.all()
        serializers = DrinkDetailsSerializer(side, many=True)
        return Response({"Drink List":serializers.data})
    
    def post(self, request):
        errors = []
        required_fields = ['name', 'description', 'price']

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field]= field_required_error
            if len(errors) != 0:
                return Response(data={'status':bad_request, 'message':errors}, status=bad_request)
                    
        nameInput = request.data['name']

        if 'name' in request.data and Sidedish.objects.filter(name = nameInput).count() != 0:
            errors['name']=(f"The product {nameInput} is already in the list!")
        if len(errors) != 0:
                return Response(data={'status':bad_request, 'message':errors}, status=bad_request)
    
        uid = uuid.uuid4().hex[-8:]
        request.data._mutable=True
        request.data['uid'] = uid
        request.data._mutable=False
        serializers = SideDetailsSerializer(data=request.data)
        print(uid)
        if serializers.is_valid():
            #serializers.save()
            return Response(data={"status": created, "message": product_added, "Food List":serializers.data})
        return Response(serializers.errors, status=bad_request)

