from django.contrib import admin
from .models import *

# Register your models here.

class Product(admin.ModelAdmin):
    readonly_fields = ('product_id','date_created','date_updated')

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('clear_picture'):
            obj.delete_image()

        obj.save()

admin.site.register(Food, Product)
admin.site.register(Drink, Product)
admin.site.register(Side, Product)

admin.site.register(CustomUser)
admin.site.register(Wallet)

admin.site.register(CustomerFeedback)
