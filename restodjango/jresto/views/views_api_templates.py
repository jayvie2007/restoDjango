from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from jresto.models import Food,Drink,Side, CustomerFeedback
from jresto.serializers.product_serializers import FoodGetSerializer, DrinkGetSerializer, SideGetSerializer, FeedbackGetSerializer
from jresto.utils import *

from constants.status_code import *

from datetime import date

class GetCustomerFeedback(APIView):
    def get(self, request):
        customer_feedback = CustomerFeedback.objects.all()
        feedback_serializers = FeedbackGetSerializer(customer_feedback, many=True)
        return Response({"Feedback": feedback_serializers.data})

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

        if 'name' in request.data and Food.objects.filter(name = product_name).count() != 0:
            errors['name']=(f"The product {product_name} is already added!")
            return Response(data={"message":errors}, status=bad_request)

        product_uid = f"food__{generate_uid()}"
        request.data._mutable=True
        request.data['product_id'] = product_uid
        request.data._mutable=False
        food_serializers = FoodGetSerializer(data=request.data)
        if food_serializers.is_valid():
            food_serializers.save()
            return Response(data={"status": created, "message": register_success, "Food Added":food_serializers.data})
        return Response(food_serializers.errors, status=bad_request)

class PutFoodAPIView(APIView):
    def get(self, request, product_id):
        try:
            foods = Food.objects.get(product_id = product_id)
        except Food.DoesNotExist:
            return Response(data={'status': not_found, 'message':does_not_exist})
        food_serializers = FoodGetSerializer(foods)
        return Response({"Food Item":food_serializers.data})

    def put(self, request, product_id):
        errors = {}
        required_fields = ['name', 'description', 'price',]

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        try:
            foods = Food.objects.get(product_id = product_id)
        except Food.DoesNotExist:
            return Response(data={'status': not_found, 'message': does_not_exist})
        
        product_updated = date.today()
        request.data._mutable=True
        request.data['date_updated'] = product_updated
        request.data._mutable=False
        food_serializers = FoodGetSerializer(foods, data=request.data)
        if food_serializers.is_valid():
            food_serializers.save()
            return Response(data={'status':ok, 'message':updated, "Food List":food_serializers.data})
        return Response(food_serializers.errors, status=bad_request)
    
class DeleteFoodAPIView(APIView):    
    def delete(self, request, product_id):
        try:
            foods = Food.objects.get(product_id = product_id)
        except Food.DoesNotExist:
            return Response({"status": not_found, 'message': does_not_exist})
        
        foods.delete()
        return Response(data={'status':no_content, 'message':deleted})

class GetDrinkAPIView(APIView):
    def get(self, request):
        drinks = Drink.objects.all()
        drink_serializers = DrinkGetSerializer(drinks, many=True)
        return Response({"Drink List": drink_serializers.data})

class PostDrinkAPIView(APIView):
    def post(self, request):
        errors = {}
        required_fields = ['name', 'description', 'price',]

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        product_name = request.data['name']

        if 'name' in request.data and Drink.objects.filter(name = product_name).count() != 0:
            errors['name']=(f"The product {product_name} is already added!")
            return Response(data={"message":errors}, status=bad_request)

        product_uid = f"drinks___{generate_uid()}"
        request.data._mutable=True
        request.data['product_id'] = product_uid
        request.data._mutable=False
        drink_serializers = DrinkGetSerializer(data=request.data)
        if drink_serializers.is_valid():
            drink_serializers.save()
            return Response(data={"status": created, "message": register_success, "Drink Added":drink_serializers.data})
        return Response(drink_serializers.errors, status=bad_request)

class PutDrinkAPIView(APIView):    
    def put(self, request, product_id):
        errors = {}
        required_fields = ['name', 'description', 'price',]

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        try:
            drinks = Drink.objects.get(product_id = product_id)
        except Food.DoesNotExist:
            return Response(data={'status': not_found, 'message': does_not_exist})
        
        product_updated = date.today()
        request.data._mutable=True
        request.data['date_updated'] = product_updated
        request.data._mutable=False
        drink_serializers = FoodGetSerializer(drinks, data=request.data)
        if drink_serializers.is_valid():
            drink_serializers.save()
            return Response(data={'status':ok, 'message':updated, "Drink List":drink_serializers.data})
        return Response(drink_serializers.errors, status=bad_request)
    
class DeleteDrinkAPIView(APIView):    
    def delete(self, request, product_id):
        try:
            drinks = Drink.objects.get(product_id = product_id)
        except Drink.DoesNotExist:
            return Response({"status": not_found, 'message': does_not_exist})
        
        drinks.delete()
        return Response(data={'status':no_content, 'message':deleted})

class GetSideAPIView(APIView):
    def get(self, request):
        sides = Drink.objects.all()
        side_serializers = DrinkGetSerializer(sides, many=True)
        return Response({"Drink List": side_serializers.data})

class PostSideAPIView(APIView):    
    def post(self, request):
        errors = {}
        required_fields = ['name', 'description', 'price',]

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        product_name = request.data['name']

        if 'name' in request.data and Side.objects.filter(name = product_name).count() != 0:
            errors['name']=(f"The product {product_name} is already added!")
            return Response(data={"message":errors}, status=bad_request)

        product_uid = f"side__{generate_uid()}"
        request.data._mutable=True
        request.data['product_id'] = product_uid
        request.data._mutable=False
        side_serializers = SideGetSerializer(data=request.data)
        if side_serializers.is_valid():
            side_serializers.save()
            return Response(data={"status": created, "message": register_success, "Side Added":side_serializers.data})
        return Response(side_serializers.errors, status=bad_request)

class PutSideAPIView(APIView):
    def put(self, request, product_id):
        errors = {}
        required_fields = ['name', 'description', 'price',]

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        try:
            sides = Side.objects.get(product_id = product_id)
        except Food.DoesNotExist:
            return Response(data={'status': not_found, 'message': does_not_exist})
        
        product_updated = date.today()
        request.data._mutable=True
        request.data['date_updated'] = product_updated
        request.data._mutable=False
        side_serializers = FoodGetSerializer(sides, data=request.data)
        if side_serializers.is_valid():
            side_serializers.save()
            return Response(data={'status':ok, 'message':updated, "Side List":side_serializers.data})
        return Response(side_serializers.errors, status=bad_request)
    
class DeleteSideAPIView(APIView):  
    def delete(self, request, product_id):
        try:
            sides = Side.objects.get(product_id = product_id)
        except Drink.DoesNotExist:
            return Response({"status": not_found, 'message': does_not_exist})
        
        sides.delete()
        return Response(data={'status':no_content, 'message':deleted})