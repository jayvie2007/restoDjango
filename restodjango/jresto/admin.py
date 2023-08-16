from django.contrib import admin
from .models import *

# Register your models here.

class Product_Admin(admin.ModelAdmin):
    readonly_fields = ('product_id','date_created','date_updated')

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('clear_picture'):
            obj.delete_image()

        obj.save()
        
class User(admin.ModelAdmin):
    readonly_fields =('uid',)

admin.site.register(Product, Product_Admin)

admin.site.register(CustomUser, User)
admin.site.register(Customer)

admin.site.register(CustomerFeedback)
