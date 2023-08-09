from jresto.models import CustomUser, Customer
from rest_framework import serializers

class CustomerGetSerializer(serializers.ModelSerializer):
    cash = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['uid', 'username' ,'first_name', 'middle_name', 'last_name', 'gender', 'email', 'contact_number', 'save_password', 'cash', 'date_created', 'date_updated',]

    def get_cash(self, obj):
            # Retrieve the associated Wallet instance for the current customer object
            wallet_instance = Customer.objects.get(customer=obj)
            # Get the cash value from the Wallet instance
            return wallet_instance.cash
class AdminGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']