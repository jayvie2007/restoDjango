from jresto.models import CustomAdmin, CustomerDetails, Wallet
from rest_framework import serializers

class CustomerGetSerializer(serializers.ModelSerializer):
    cash = serializers.SerializerMethodField()

    class Meta:
        model = CustomerDetails
        fields = ['uid', 'first_name', 'middle_name', 'last_name', 'email', 'contact_number', 'save_password', 'cash', 'date_created', 'date_updated',]

    def get_cash(self, obj):
            # Retrieve the associated Wallet instance for the current customer object
            wallet_instance = Wallet.objects.get(customer=obj)
            # Get the cash value from the Wallet instance
            return wallet_instance.cash
class AdminGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAdmin
        fields = '__all__'

class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAdmin
        fields = ['username', 'email', 'password']