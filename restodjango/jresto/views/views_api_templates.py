from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from jresto.models import Product, CustomerFeedback
from jresto.serializers.product_serializers import ProductGetSerializer, FeedbackGetSerializer
from jresto.utils import *

from constants.status_code import *

from datetime import date

class GetCustomerFeedback(APIView):
    def get(self, request):
        customer_feedback = CustomerFeedback.objects.all()
        feedback_serializers = FeedbackGetSerializer(customer_feedback, many=True)
        return Response({"Feedback": feedback_serializers.data})

class GetProductAPIView(APIView):
    def post(self, request):
        errors = {}
        required_fields = ['product_type',]
        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        product_type = request.data['product_type']

        if product_type == "Meal":
            product = Product.objects.filter(product_type="Meal")
            product_serializers = ProductGetSerializer(product, many=True)
            return Response({"Food List": product_serializers.data})
        elif product_type == "Drink":
            product = Product.objects.filter(product_type="Drink")
            product_serializers = ProductGetSerializer(product, many=True)
            return Response({"Drink List": product_serializers.data})
        elif product_type == "Side":
            product = Product.objects.filter(product_type="Side")
            product_serializers = ProductGetSerializer(product, many=True)
            return Response({"Side List": product_serializers.data})
        else:
            product = Product.objects.all()
            product_serializers = ProductGetSerializer(product, many=True)
            return Response({"Product List": product_serializers.data})

class PostProductAPIView(APIView):
    def post(self, request):
        errors = {}
        required_fields = ['name', 'description', 'price', 'product_type']

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        product_name = request.data['name']
        product_type = request.data['product_type']

        if  product_type == "Meal":
            if 'name' in request.data and Product.objects.filter(name=product_name, product_type="Meal").count() != 0:
                errors['name']=(f"The product {product_name} is already added!")
                return Response(data={"message":errors}, status=bad_request)

            product_uid = f"food__{generate_uid()}"
            request.data._mutable=True
            request.data['product_id'] = product_uid
            request.data._mutable=False
            product_serializers = ProductGetSerializer(data=request.data)
            if product_serializers.is_valid():
                product_serializers.save()
                return Response(data={"status": created, "message": register_success, "Food Added":product_serializers.data})
            return Response(product_serializers.errors, status=bad_request)
        
        elif  product_type == "Drink":
            if 'name' in request.data and Product.objects.filter(name=product_name, product_type="Drink").count() != 0:
                errors['name']=(f"The product {product_name} is already added!")
                return Response(data={"message":errors}, status=bad_request)

            product_uid = f"drink__{generate_uid()}"
            request.data._mutable=True
            request.data['product_id'] = product_uid
            request.data._mutable=False
            product_serializers = ProductGetSerializer(data=request.data)
            if product_serializers.is_valid():
                product_serializers.save()
                return Response(data={"status": created, "message": register_success, "Drink Added":product_serializers.data})
            return Response(product_serializers.errors, status=bad_request)
        
        elif  product_type == "Side":
            if 'name' in request.data and Product.objects.filter(name=product_name, product_type="Side").count() != 0:
                errors['name']=(f"The product {product_name} is already added!")
                return Response(data={"message":errors}, status=bad_request)

            product_uid = f"side__{generate_uid()}"
            request.data._mutable=True
            request.data['product_id'] = product_uid
            request.data._mutable=False
            product_serializers = ProductGetSerializer(data=request.data)
            if product_serializers.is_valid():
                product_serializers.save()
                return Response(data={"status": created, "message": register_success, "Side Added":product_serializers.data})
            return Response(product_serializers.errors, status=bad_request)
        return Response(data={"message":"The product type inputted is not in the list (Meal, Drink, Side)"}, status=bad_request)

class PutProductAPIView(APIView):
    def get(self, request, product_id):
        try:
            products = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response(data={'status': not_found, 'message':does_not_exist})
        product_serializers = ProductGetSerializer(products)
        return Response({"Food Item":product_serializers.data})

    def put(self, request, product_id):
        errors = {}
        required_fields = ['name', 'description', 'price',]

        for required_field in required_fields:
            if required_field not in request.data:
                errors[required_field] = field_required_error
            if len(errors) != 0:
                return Response(data={"status":bad_request, 'message':errors}, status=bad_request)
            
        try:
            products = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response(data={'status': not_found, 'message': does_not_exist})
        
        product_updated = date.today()
        request.data._mutable=True
        request.data['date_updated'] = product_updated
        request.data._mutable=False
        product_serializers = ProductGetSerializer(products, data=request.data)
        if product_serializers.is_valid():
            product_serializers.save()
            return Response(data={'status':ok, 'message':updated, "Food List":product_serializers.data})
        return Response(product_serializers.errors, status=bad_request)
    
class DeleteProductAPIView(APIView):    
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({"status": not_found, 'message': does_not_exist})
        
        product.delete()
        return Response(data={'status':no_content, 'message':deleted})
