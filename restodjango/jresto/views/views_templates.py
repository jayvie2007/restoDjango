from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required

from jresto.models import CustomUser, CustomerFeedback, Food, Drink, Side
from jresto.utils import *


from constants.status_code import *

from datetime import date

def index(request):
    return render(request, 'customer/index.html')

def menu(request):
    return render(request, 'customer/menu.html')

def food(request):
    foods = Food.objects.all()
    
    return render(request, 'customer/menu/food.html', {
        'foods':foods,
    })

def drink(request):
    drinks = Drink.objects.all()
    return render(request, 'customer/menu/drink.html', {
        'drinks':drinks,
    })

def side(request):
    sides = Side.objects.all()
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
            date_created = date.today(),
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
            print(user_pass)
            users.first_name = user_first_name
            users.middle_name = user_middle_name
            users.last_name = user_last_name
            users.password = make_password(user_pass)
            users.save_password = user_pass
            users.date_updated = date.today()
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
            print(users.username)
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
    return render(request, 'admin/menu.html')

def admin_menu_product(request):
    foods = Food.objects.all()
    drinks = Drink.objects.all()
    sides = Side.objects.all()

    context = {'foods': foods, 'drinks':drinks, 'sides':sides,}
    return render(request, 'admin/display_product.html', context)

def admin_add_menu(request):
    if request.method =="POST":
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_type = request.POST['product_type']
        product_description = request.POST['product_description']
        product_image = request.POST['product_image']
        product_uid = generate_uid()

        print("Type: ", product_type)
        if product_type == "Meal":
            if product_name and Food.objects.filter(name=product_name).count() != 0:
                message=(f"{product_name} is currently existing in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':False,
                })
            else:
                new_products = Food(
                    product_id = f"food__{product_uid}",
                    name = product_name,
                    price = product_price,
                    description = product_description,
                    #picture = product_image,
                    date_created = date.today(),
                )
                new_products.save()
                print("Meal success")
                message=(f"{product_name} has been added in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'success':True,
                    'message':message,
                })
        
        elif product_type == "Drink":
            if product_name and Drink.objects.filter(name=product_name).count() != 0:
                message=(f"{product_name} is currently existing in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':False,
                })
            else:  
                new_products = Drink(
                    product_id = f"drink__{product_uid}",
                    name = product_name,
                    price = product_price,
                    description = product_description,
                    #picture = product_image,
                    date_created = date.today(),
                )
                new_products.save()
                print("Drink")
                message=(f"{product_name} has been added in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':True,
                })
    
        elif product_type == "Side":
            if product_name and Side.objects.filter(name=product_name).count() != 0:
                message=(f"{product_name} is currently existing in {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message':message,
                    'success':False,
                })
            else:
                new_products = Side(
                    product_id = f"side__{product_uid}",
                    name = product_name,
                    price = product_price,
                    description = product_description,
                    #picture = product_image,
                    date_created = date.today(),
                )
                new_products.save()
                print("Side")
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
    foods = Food.objects.all()
    drinks = Drink.objects.all()
    sides = Side.objects.all()

    context = {'foods': foods, 'drinks':drinks, 'sides':sides,}
    print(context)
    return render(request, 'admin/display_product.html', context)

def admin_edit_menu(request, product_id):
    pass

def admin_delete_menu(request, product_id):
    pass