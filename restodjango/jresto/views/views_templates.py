from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from jresto.models import CustomerFeedback, CustomerDetails, Food, Drink, Side
from jresto.utils import *

from constants.status_code import *

from datetime import date

def index(request):
    return render(request, 'customer/index.html')

def menu(request):
    return render(request, 'customer/menu.html')

def food(request):
    meal = Food.objects.all()
    return render(request, 'customer/menu/food.html', {
        'meal':meal,
    })

def drink(request):
    drink = Drink.objects.all()
    return render(request, 'customer/menu/drink.html', {
        'drink':drink,
    })

def side(request):
    side = Side.objects.all()
    return render(request, 'customer/menu/side.html', {
        'side':side,
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

def register(request):
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
            if CustomerDetails.objects.filter(username = customer_username):
                print("user exist")
                return render(request, 'customer/authentication/register.html', {
                    'register_error': True,
                    'message': username_exist,
                })
            if CustomerDetails.objects.filter(email = customer_email):
                print("email exist")
                return render(request, 'customer/authentication/register.html', {
                    'register_error': True,
                    'message': email_exist,
                })
            else:
                new_customer = CustomerDetails.objects.create(
                    uid = f"customer__{uid}",
                    first_name = customer_firstname,
                    middle_name = customer_middlename,
                    last_name = customer_lastname,
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

def login(request):
    return render(request, 'customer/authentication/login.html')

