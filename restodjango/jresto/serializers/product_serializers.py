from jresto.models import Product, CustomerFeedback
from rest_framework import serializers

class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FeedbackGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFeedback
        fields ='__all__'
