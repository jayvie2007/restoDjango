from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Food)
admin.site.register(Drink)
admin.site.register(Side)

admin.site.register(CustomerDetails)
admin.site.register(Wallet)
