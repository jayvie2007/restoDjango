from django.contrib import admin
from .models import *

# Register your models here.

class Product(admin.ModelAdmin):
    readonly_fields = ('product_id','date_created','date_updated')

admin.site.register(Food, Product)
admin.site.register(Drink)
admin.site.register(Side)

admin.site.register(CustomerDetails)
admin.site.register(Wallet)
