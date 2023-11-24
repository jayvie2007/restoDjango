from django.contrib import admin
from .models import *

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'cash',
    )


class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'contact_number',
        'message',
        'date_created',
    )


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = (
        'product_id',
        'date_created',
        'date_updated'
    )

    list_display = (
        'product_type',
        'name',
        'price',
        'date_created',
        'date_updated',
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('clear_picture'):
            obj.delete_image()

        obj.save()
        

class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields =(
        'uid',
        'date_created',
        'date_updated',
        'password'
    )
    
    exclude = (
        'user_permissions',
        'groups',
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    )
    
    fields = (
        'username',
        'password',
        'save_password',
        'first_name',
        'middle_name',
        'last_name',
        'gender',
        'email',
        'contact_number',
        'user_level',
        'uid',
        'date_created',
        'date_updated',

    )



class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = (
        'date_created', 
        'date_completed'
    )

    list_display = (
        'order',
        'product',
        'quantity',
        'date_created',
        'date_completed',
    )

    raw_id_fields = (
        'order',
        'product',
    )
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = (
        'date_created', 
        'date_completed', 
        'total_bill'
    )
    
    list_display = (
        'id',
        'customer',
        'total_bill',
        'status',
        'transaction_id',
        'complete',
        'date_created',
        'date_completed'
    )


class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'address',
        'province',
        'city',
        'barangay',
        'zip_code',
        'contact_number',
        'date_created',
    )    


admin.site.register(Product, ProductAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CustomerFeedback, CustomerFeedbackAdmin)
admin.site.register(DeliveryInfo, DeliveryInfoAdmin)
