from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from datetime import date
from django.utils.timezone import now
# Create your models here.

class Food(models.Model):
    product_id = models.CharField(max_length=8)
    name = models.CharField(max_length=25)
    picture = models.ImageField(blank=True, null=True)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default="")
    date_created = models.DateField(editable=False, default=date.today)
    date_updated = models.DateField(editable=False, default="")

    def __str__(self):
        return f"Dishes: {self.name}"    
    
class Drink(models.Model):
    product_id = models.CharField(max_length=8)
    name = models.CharField(max_length=25, default="")
    picture = models.ImageField(blank=True, null=True)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default="")
    date_created = models.DateField(editable=False, default=now)
    date_updated = models.DateField(editable=False, default="")

    def __str__(self):
        return f"Drinks: {self.name}"  
    
class Side(models.Model):
    product_id = models.CharField(max_length=8)
    name = models.CharField(max_length=25, default="")
    picture = models.ImageField(blank=True, null=True)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100, default="")
    date_created = models.DateTimeField(editable=False, default=now)
    date_updated = models.DateField(editable=False, default="")

    def __str__(self):
        return f"Side: {self.name}"

class CustomAdmin(AbstractUser):
    uid = models.CharField(max_length=8, default="")    
    middle_name = models.CharField(max_length=255, null=True, blank=True, default="")
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_set')
    
    def __str__(self):
        return self.username + " " + self.email

class CustomerDetails (AbstractUser):
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    contact_number_regex = r'^(\+[0-9]{1,12})|[0-9]{1,11}$'
    contact_number_validator = RegexValidator(
        regex=contact_number_regex,
        message='Contact number must start with + and include only digits.'
    )
    
    uid = models.CharField(max_length=8, editable=False)
    middle_name = models.CharField(max_length=50, default="")
    extension_name = models.CharField(max_length=50, default="", null=True)
    gender = models.CharField(max_length=6, choices=gender_choices)
    contact_number = models.CharField(max_length=12, validators=[contact_number_validator])
    groups = models.ManyToManyField(Group, blank=True, related_name='CustomerDetails')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='CustomerDetails')
    date_created = models.DateField(editable=False, default=now)
    date_updated = models.DateField(editable=False, default="")

    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the instance is being created for the first time
        super().save(*args, **kwargs)  # Call the original save() method

        if created:
            Wallet.objects.create(
                customer=self,
                cash=0
            )
    
class Wallet(models.Model):
    customer = models.OneToOneField(
        CustomerDetails,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='wallet'
    )
    cash = models.IntegerField(default=0)

    def __str__(self):
        return f"Wallet: {self.customer.first_name} {self.customer.last_name}"