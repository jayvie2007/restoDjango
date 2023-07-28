from django.shortcuts import render
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.response import Response

from jresto.models import Food,Drink,Side
from jresto.serializers.product_serializers import FoodGetSerializer, DrinkGetSerializer, SideGetSerializer
from jresto.utils import *

from constants.status_code import *


class GetFoodAPIView(APIView):
    def get(self, request):
        foods = Food.objects.all()
        food_serializers = FoodGetSerializer(foods, many=True)
        return Response({"Food List": food_serializers.data})

class PostFoodAPIView(APIView):
    def post(self, request):
        errors = {}
        required_fields = ['name', 'description', 'price',]

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        product_name = request.data['name']
        product_price = request.data['price']
        product_description = request.data['description']

        try:
            if 'name' in request.data and Food.objects.filter(name = product_name).count() != 0:
                errors['name']=(f"The product {product_name} is already added!")
                return Response(data={"message":errors}, status=bad_request)
        except:
            product_uid = generate_fooduid()
            request.data._mutable=True
            request.data['uid'] = product_uid
            request.data._mutable=False
            food_serializers = FoodGetSerializer(data=request.data)
            if food_serializers.is_valid():
                #food_serializers.save()
                return Response(data={"status": created, "message": register_success, "Users":food_serializers.data})
            return Response(food_serializers.errors, status=bad_request)

class PutFoodAPIView(APIView):
    def put(self, request):
        pass

class DeleteFoodAPIView(APIView):    
    def delete(self, request):
        pass

class GetDrinkAPIView(APIView):
    def get(self, request):
        drinks = Drink.objects.all()
        drink_serializers = DrinkGetSerializer(drinks, many=True)
        return Response({"Food List": drink_serializers.data})

class PostDrinkAPIView(APIView):
    def menu_add_drink(self, request):
        pass

class PutDrinkAPIView(APIView):    
    def menu_edit_drink(self, request):
        pass
    
class DeleteDrinkAPIView(APIView):    
    def menu_delete_drink(self, request):
        pass

class GetSideAPIView(APIView):
    def menu_get_side(self, request):
        pass

class PostSideAPIView(APIView):    
    def menu_add_side(self, request):
        pass

class PutSideAPIView(APIView):
    def menu_edit_side(self, request):
        pass
    
class DeleteSideAPIView(APIView):  
    def menu_delete_side(self, request):
        pass
