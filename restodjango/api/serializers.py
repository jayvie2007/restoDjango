from rest_framework import serializers

from jresto.models import Food, Drink, Side

class FoodDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name', 'price' ,'description']

class DrinkDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ['name', 'price' ,'description']

class SideDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Side
        fields = ['name', 'price' ,'description']