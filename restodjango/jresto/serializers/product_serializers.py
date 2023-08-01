from jresto.models import Food, Drink, Side, CustomerFeedback
from rest_framework import serializers

class FoodGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class DrinkGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = '__all__'

class SideGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Side
        fields = '__all__'

class FeedbackGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFeedback
        fields ='__all__'
