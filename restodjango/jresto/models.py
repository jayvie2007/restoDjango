from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

from datetime import date

from jresto.utils import *

import os
# Create your models here.

gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

permission_choices = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
)
product_choices = (
    ('Meal', 'Meal'),
    ('Drink', 'Drink'),
    ('Side', 'Side'),
)

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
    product_type = models.CharField(max_length=15, choices=product_choices, default="")
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
    gender = models.CharField(max_length=6, choices=gender_choices, blank=True)
    contact_number = models.CharField(max_length=12, validators=[contact_number_validator], blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='CustomerDetails')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='CustomerDetails')
    save_password = models.CharField(max_length=20, default="", blank=True)
    user_level = models.CharField(max_length=20, choices=permission_choices)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user_level}: {self.first_name} {self.last_name}"
    
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
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)
    complete = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_completed = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.customer.first_name}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_completed = models.DateField(auto_now=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return f"{self.order.customer}, Product: {self.product.name}, Quantity: {self.quantity}"
