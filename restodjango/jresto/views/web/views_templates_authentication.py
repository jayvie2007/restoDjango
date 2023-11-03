from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from jresto.models import CustomUser, Order
from jresto.utils import generate_uid

from constants.status_code import *


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
            if CustomUser.objects.filter(username=customer_username):
                return render(request, 'customer/authentication/register.html', {
                    'register_error': True,
                    'message': username_exist,
                })

            if CustomUser.objects.filter(email=customer_email):
                return render(request, 'customer/authentication/register.html', {
                    'register_error': True,
                    'message': email_exist,
                })
            else:
                CustomUser.objects.create(
                    uid=f"customer__{uid}",
                    first_name=customer_firstname,
                    middle_name=customer_middlename,
                    last_name=customer_lastname,
                    user_level="Customer",
                    gender=customer_gender,
                    email=customer_email,
                    contact_number=customer_number,
                    username=customer_username,
                    password=make_password(customer_password),
                    save_password=customer_password,
                )
                return redirect('user_login')
        else:
            return render(request, 'customer/authentication/register.html', {
                'register_error': True,
                'message': password_not_match
            })
    return render(request, 'customer/authentication/register.html')


@login_required
def edit_customer(request, uid):
    customer_id = request.user.id
    customer = CustomUser.objects.get(id=customer_id)
    orders = Order.objects.filter(customer=customer, complete=False)

    total_cart_items = orders.aggregate(Sum('orderitem__quantity'))[
        'orderitem__quantity__sum']

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
                'message': "Please enter a password!",
                'cart_quantity': total_cart_items,
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
                'message': "Success Updating",
                'cart_quantity': total_cart_items,
            })
        else:
            return render(request, 'customer/authentication/edit.html', {
                'users': users,
                'success': False,
                'message': password_not_match,
                'cart_quantity': total_cart_items,
            })
    else:
        users = CustomUser.objects.get(uid=uid)
        return render(request, 'customer/authentication/edit.html', {
            'users': users,
            'cart_quantity': total_cart_items,
        })


def login_customer(request):
    if request.method == 'POST':
        customer_user = request.POST['customer_user']
        customer_pass = request.POST['customer_pass']
        users = authenticate(
            request, username=customer_user, password=customer_pass)

        if users is not None:
            login(request, users)
            if request.user.user_level == "Admin":
                return redirect('admin_menu')
            else:
                return redirect('index')
        else:
            return render(request, 'customer/authentication/login.html', {
                'success': False,
            })
    return render(request, 'customer/authentication/login.html')


def logout_customer(request):
    logout(request)
    return redirect('user_login')
