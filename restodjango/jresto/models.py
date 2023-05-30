from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

# Create your models here.
class Food(models.Model):
    product_id = models.CharField(max_length=8)
    name = models.CharField(max_length=25, default="")
    picture = models.ImageField(default="")
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"Dishes: {self.name}"    
    
class Drink(models.Model):
    product_id = models.CharField(max_length=8)
    name = models.CharField(max_length=25, default="")
    picture = models.ImageField(default="")
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"Drinks: {self.name}"  
    
class Sidedishes(models.Model):
    product_id = models.CharField(max_length=8)
    name = models.CharField(max_length=25, default="")
    picture = models.ImageField(default="")
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"Side Dishes: {self.name}"

class CustomerDetails (AbstractUser):
    gender_choices = (
        'male', 'Male',
        'female', 'Female',
        'other', 'Other',
    )

    contact_number_regex = r'^(\+[0-9]{1,12})|[0-9]{1,11}$'
    contact_number_validator = RegexValidator(
        regex=contact_number_regex,
        message='Contact number must start with + and include only digits.'
    )
    
    uid = models.CharField(max_length=8, editable=False)
    middle_name = models.CharField(max_length=50, default="")
    extension_name = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=6, choices=gender_choices)
    contact_number = models.CharField(max_length=12, validators=[contact_number_validator])
    groups = models.ManyToManyField(Group, blank=True, related_name='CustomerDetails')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='CustomerDetails')

    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}"
    
class Wallet(models.model):
    first_name = models.OneToOneField(CustomerDetails, on_delete=models.CASCADE)
    middle_name = models.OneToOneField(CustomerDetails, on_delete=models.CASCADE)
    last_name = models.OneToOneField(CustomerDetails, on_delete=models.CASCADE)
    cash = models.IntegerField(default=0)

      
    
