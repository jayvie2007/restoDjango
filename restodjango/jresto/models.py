from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils import timezone

from datetime import date

from jresto.choices import *
from jresto.utils import *

import os


contact_number_regex = r'^(\+[0-9]{1,12})|[0-9]{1,11}$'
contact_number_validator = RegexValidator(
    regex=contact_number_regex,
    message='Contact number must start with + and include only digits.'
)


class CustomerFeedback(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    contact_number = models.CharField(max_length=12, validators=[contact_number_validator])
    message = models.CharField(max_length=500)
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.id}. {self.name}"

class Product(models.Model):
    product_id = models.CharField(max_length=16, default="")
    product_type = models.CharField(max_length=15, choices=PRODUCT_CHOICES, default="")
    name = models.CharField(max_length=25)
    picture = models.ImageField(blank=True, null=True)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default="")
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.product_type}: {self.name}" 

    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url   
    
    def delete_image(self):
        if self.picture:
            if os.path.exists(self.picture.path):
                os.remove(self.picture.path)
            self.picture = None
            self.save(update_fields=['picture'])
    

class CustomUser (AbstractUser):
    uid = models.CharField(max_length=20, editable=False)
    middle_name = models.CharField(max_length=50, default="", blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    contact_number = models.CharField(max_length=12, validators=[contact_number_validator], blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='CustomerDetails')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='CustomerDetails')
    save_password = models.CharField(max_length=20, default="", blank=True)
    user_level = models.CharField(max_length=20, choices=PERMISSION_CHOICES)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the instance is being created for the first time
        super().save(*args, **kwargs)  # Call the original save() method

        if created and self.user_level == "Customer":
            Customer.objects.create(
                customer=self,
                cash=0
            )

    class Meta:
        verbose_name = "User"


class Customer(models.Model):
    customer = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True,related_name='wallet')
    cash = models.IntegerField(default=0)

    def __str__(self):
        return f"Wallet: {self.customer.first_name} {self.customer.last_name}"
    
class Order(models.Model):
    complete = models.BooleanField(default=False)
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)
    total_bill = models.IntegerField(null=True, default=0)
    status = models.CharField(choices=PROCESS_TYPE_CHOICES, max_length=20, default="Pending")
    date_created = models.DateField(auto_now_add=True)
    date_completed = models.DateField(null=True)
    

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    def __str__(self):
        return f"{self.id}. {self.customer.first_name} {self.customer.last_name}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_completed = models.DateField(null=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return f"{self.order.id}. {self.order.customer}, Product: {self.product.name}, Quantity: {self.quantity}"


class DeliveryInfo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    email = models.EmailField()
    contact_number = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Delivery: {self.id}. {self.first_name} {self.last_name}"



class TransactionHistory(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    transaction_type = models.CharField(choices=ALL_TRANSACTION_TYPE, max_length=50, blank=False, null=False)
    amount = models.DecimalField(max_digits=100, default=0, decimal_places=0, null=True, blank=True)
    before_amount = models.DecimalField(max_digits=100, default=0, decimal_places=0, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=100, default=0, decimal_places=0, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.transaction_type} {self.customer_id}'
