from jresto.models import CustomAdmin
from rest_framework import serializers

class AdminGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAdmin
        fields = '__all__'

class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAdmin
        fields = ['username', 'email', 'password']