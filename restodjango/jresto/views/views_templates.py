from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from jresto.models import CustomUser, CustomerFeedback, Product
from jresto.utils import *

from constants.status_code import *

from datetime import date
import os

def index(request):
    return render(request, 'customer/index.html')

def menu(request):
    return render(request, 'customer/menu.html')

def food(request):
    foods = Product.objects.filter(product_type="Meal")
    return render(request, 'customer/menu/food.html', {
        'foods':foods,
    })

def drink(request):
    drinks = Product.objects.filter(product_type="Drink")
    return render(request, 'customer/menu/drink.html', {
        'drinks':drinks,
    })

def side(request):
    sides = Product.objects.filter(product_type="Side")
    return render(request, 'customer/menu/side.html', {
        'sides':sides,
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST['feedback_name']
        email = request.POST['feedback_email']
        contact_number = request.POST['feedback_number']
        message = request.POST['feedback_message']

        new_message = CustomerFeedback.objects.create(
            name = name,
            email = email,
            contact_number = contact_number,
            message = message,
        )

        return render(request, 'customer/contact.html', {
            'message':message_success,
            'submit':True,
        })
    return render(request, 'customer/contact.html')

def register_customer(request):
    if request.method == 'POST':
        customer_firstname = request.POST['customer_firstname']
        customer_middlename = request.POST['customer_middlename']
        customer_lastname = request.POST['customer_lastname']
        customer_gender = request.POST['customer_gender']
        customer_username = request.POST['customer_username']
        customer_email = request.POST['customer_email']
        customer_number = request.POST['customer_number']
        customer_password = request.POST['customer_password']
        customer_confirm_password = request.POST['customer_confirm_password']
        uid = generate_uid()

        if customer_gender == "Select Gender":
            return render(request, 'customer/authentication/register.html', {
                    'register_error': True,
                    'message': "Please select a gender",
                })
        if customer_password == customer_confirm_password:
            if CustomUser.objects.filter(username = customer_username):
                print("user exist")
                return render(request, 'customer/authentication/register.html', {
                    'register_error': True,
                    'message': username_exist,
                })
            if CustomUser.objects.filter(email = customer_email):
                print("email exist")
                return render(request, 'customer/authentication/register.html', {
                    'register_error': True,
                    'message': email_exist,
                })
            else:
                new_customer = CustomUser.objects.create(
                    uid = f"customer__{uid}",
                    first_name = customer_firstname,
                    middle_name = customer_middlename,
                    last_name = customer_lastname,
                    user_level = "Customer",
                    gender = customer_gender,
                    email = customer_email,
                    contact_number = customer_number,
                    username = customer_username,
                    password = make_password(customer_password),
                    save_password = customer_password,
                )
                print("Successfully created a new customer")
                return redirect('user_login')
        else:
            print("wrong pass")
            return render(request, 'customer/authentication/register.html', {
                'register_error':True,
                'message': password_not_match
            })
    return render(request, 'customer/authentication/register.html')

@login_required
def edit_customer(request, uid):
    if request.method == 'POST':
        users = CustomUser.objects.get(uid=uid)
        user_first_name = request.POST['user_first_name']
        user_middle_name = request.POST['user_middle_name']
        user_last_name = request.POST['user_last_name']
        user_pass = request.POST['user_pass']
        user_confirm_pass = request.POST['user_confirm_pass']

        if not user_pass and not user_confirm_pass:
            return render(request, 'customer/authentication/edit.html', {
            'users': users,
            'success': False,
            'message':"Please enter a password!",
        })

        elif user_pass == user_confirm_pass:
            users.first_name = user_first_name
            users.middle_name = user_middle_name
            users.last_name = user_last_name
            users.password = make_password(user_pass)
            users.save_password = user_pass
            users.save()
            login(request, users)
            
            return render(request, 'customer/authentication/edit.html', {
            'users': users,
            'success': True,
            'message':"Success Updating",
            })
        else:
            return render(request, 'customer/authentication/edit.html', {
            'users': users,
            'success': False,
            'message':password_not_match,
            })
    else:
        users = CustomUser.objects.get(uid=uid)
        return render(request, 'customer/authentication/edit.html', {
            'users': users,
        })

def login_customer(request):
    if request.method == 'POST':
        customer_user = request.POST['customer_user']
        customer_pass = request.POST['customer_pass']

        users = authenticate(request, username=customer_user, password=customer_pass)
        if users is not None:
            login(request, users)
            print("customer login!")
            return redirect('index')
        else:
            print("customer failed")
            return render(request, 'customer/authentication/login.html', {
                'success':False,
            })
    return render(request, 'customer/authentication/login.html')

def logout_customer(request):
    print("logout")
    logout(request)
    return redirect('index')

def admin_menu(request):
    if not request.user.user_level == "Admin":
        return redirect('index')
    return render(request, 'admin/menu.html')

def admin_add_menu(request):
    if not request.user.user_level == "Admin":
        return redirect('index')
    if request.method =="POST":        
        try:
            product_image = request.FILES['product_image']
        except:
            product_image = None

        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_type = request.POST['product_type']
        product_description = request.POST['product_description']
        product_uid = generate_uid()

        if product_type == "Select Product Type":
            return render(request, 'admin/add_product.html', {
                    'message':"Please select a product type",
                    'success':False,
                })

        if product_type == "Meal":
            if product_name and Product.objects.filter(name=product_name, product_type=product_type).count() != 0:
                message = (f"{product_name} is currently existing in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':False,
                })
            else:
            # Handle image upload and linking
                if product_image:
                    # Check if the image already exists in MEDIA_ROOT
                    image_path = os.path.join(settings.MEDIA_ROOT, product_image.name)
                    if not default_storage.exists(image_path):
                        # If the image doesn't exist, save it
                        default_storage.save(image_path, ContentFile(product_image.read()))

                new_product = Product(
                    product_id = f"food__{product_uid}",
                    product_type = product_type,
                    name = product_name,
                    price = product_price,
                    description = product_description,
                    picture = product_image.name if product_image else None,
                )
                new_product.save()
                message = (f"{product_name} has been added in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'success':True,
                    'message':message,
                })
        
        elif product_type == "Drink":
            if product_name and Product.objects.filter(name=product_name, product_type=product_type).count() != 0:
                message = (f"{product_name} is currently existing in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':False,
                })
            else:
                if product_image:
                    # Check if the image already exists in MEDIA_ROOT
                    image_path = os.path.join(settings.MEDIA_ROOT, product_image.name)
                    if not default_storage.exists(image_path):
                        # If the image doesn't exist, save it
                        default_storage.save(image_path, ContentFile(product_image.read()))
                        
                new_products = Product(
                    product_id = f"drink__{product_uid}",
                    product_type = product_type,
                    name = product_name,
                    price = product_price,
                    description = product_description,
                    picture = product_image.name if product_image else None,
                )
                new_products.save()
                message=(f"{product_name} has been added in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':True,
                })
    
        elif product_type == "Side":
            if product_name and Product.objects.filter(name=product_name, product_type=product_type).count() != 0:
                message=(f"{product_name} is currently existing in {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':False,
                })
            else:
                if product_image:
                    # Check if the image already exists in MEDIA_ROOT
                    image_path = os.path.join(settings.MEDIA_ROOT, product_image.name)
                    if not default_storage.exists(image_path):
                        # If the image doesn't exist, save it
                        default_storage.save(image_path, ContentFile(product_image.read()))

                new_products = Product(
                    product_id = f"side__{product_uid}",
                    product_type = product_type,
                    name = product_name,
                    price = product_price,
                    description = product_description,
                    picture = product_image.name if product_image else None,
                )
                new_products.save()
                message=(f"{product_name} has been added in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':True,
                })
        message = ("Please choose a product type!")
        return render(request, 'admin/add_product.html',{
            'message':message,
            'success':False
        })
    return render(request, 'admin/add_product.html')

def admin_display_menu(request):
    if not request.user.user_level == "Admin":
        return redirect('index')
    
    if request.method == 'POST':
        no_of_display = request.POST['no_of_display']
        product_filter = request.POST['product_filter']
        product_sort = request.POST['product_sort']
        products = Product.objects.all()

        #Check no of display for pagination
        if int(no_of_display) == 10:
            page_row = 10
        elif int(no_of_display) == 15:
            page_row = 15
        else: page_row = 5
            
        #Check product to be filtered
        if product_filter == "Meal":
            products = Product.objects.filter(product_type="Meal")
        elif product_filter == "Drink":
            products = Product.objects.filter(product_type="Drink")
        elif product_filter == "Side":
            products = Product.objects.filter(product_type="Side")
        else: products = Product.objects.all()

        #Check product sort to be sorted
        if product_sort == "Date Created":
            sort = "-date_created"
        elif product_sort == "Date Updated":
            sort ="-date_updated"
        elif product_sort == "Product Type":
            sort = "product_type"
        elif product_sort == "Name":  
            sort = "name"
        else: sort = "-id"

    else:
        page_row = 5
        products = Product.objects.all()
        sort = "-id"

    pagination = Paginator(products.order_by(sort),page_row)
    page = request.GET.get('page')

    if page == None:
        product_list = pagination.get_page(page)
        page = 1
        return render(request, 'admin/display_product.html', {
        'product_list':product_list,
        'page_number':page
    })
    else: 
        product_list = pagination.get_page(page)
        return render(request, 'admin/display_product.html',{
        'product_list':product_list,
        'page_number':int(page),
        })

def admin_edit_menu(request, product_id):
    try:
        products = Product.objects.get(product_id=product_id)
    except ObjectDoesNotExist:
        raise Http404("Product does not exist")
    if request.method == 'POST':
        try:
            product_image = request.FILES['product_image']
        except:
            product_image = None

        errors = {}

        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_type = request.POST['product_type']
        product_description = request.POST['product_description']
        
        if product_image:
            # Delete the old image if it exists
            if products.picture:
                old_image_path = os.path.join(settings.MEDIA_ROOT, products.picture)
                if default_storage.exists(old_image_path):
                    default_storage.delete(old_image_path)

            # Save the new image
            image_path = os.path.join(settings.MEDIA_ROOT, product_image.name)
            default_storage.save(image_path, ContentFile(product_image.read()))
        else:
            # If no new image is provided, retain the old image path
            product_image = products.picture

        products.name = product_name
        products.price = product_price
        products.product_type = product_type
        products.description = product_description
        products.picture = product_image
        products.save()

        return render(request, 'admin/edit_product.html', {
            'products':products,
            'success':True,
            'message':"Successfully Edited!"
        })

    return render(request, 'admin/edit_product.html', {
        'products':products,
    })

def admin_delete_menu(request, product_id):
    try:
        products = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return HttpResponseRedirect(reverse('menu_product'))

    # Delete the associated image if it exists
    if products.picture:
        image_path = products.picture.path
        if default_storage.exists(image_path):
            default_storage.delete(image_path)
    products.delete()
    return HttpResponseRedirect(reverse('menu_product'))
def admin_feedback(request):
    page_row = 1
    pagination = Paginator(CustomerFeedback.objects.all().order_by('id'),page_row)
    page = request.GET.get('page')

    if page == None:
        feedback_list = pagination.get_page(page)
        page = 1
        return render(request, 'admin/check_feedback.html',{
            'feedback_list':feedback_list,
            'page_number':page,
    })
    else:
        feedback_list = pagination.get_page(page)
        return render(request, 'admin/check_feedback.html',{
            'feedback_list':feedback_list,
            'page_number':int(page),
            })

def admin_feedback_delete(request, id):
    feedbacks = CustomerFeedback.objects.get(id=id)
    feedbacks.delete()
    messages = ("Successfully Delete")
    return HttpResponseRedirect(reverse('admin_feedback'))