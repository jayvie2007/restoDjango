from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout, login

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
                return render(request, 'customer/authentication/login.html', {
                    'success':True,
                })
        else:
            print("wrong pass")
            return render(request, 'customer/authentication/register.html', {
                'register_error':True,
                'message': password_not_match
            })
    return render(request, 'customer/authentication/register.html')

def login_customer(request):
    if request.method == 'POST':
        customer_user = request.POST['customer_user']
        customer_pass = request.POST['customer_pass']

        users = authenticate(request, username=customer_user, password=customer_pass)
        if users is not None:
            login(request, users)
            print("customer login!")
            print(users.username)
            return render(request, 'customer/index.html', {
                'success':True
            })
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