from rest_framework import serializers

from jresto.models import Food, Drink, Sidedish

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
        model = Sidedish
        fields = ['name', 'price' ,'description']