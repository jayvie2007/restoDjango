from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from jresto.models import CustomAdmin, CustomerDetails
from jresto.utils import *

from constants.status_code import *


def register(request):
    if request.method == 'POST':
        admin_firstname = request.POST['admin_firstname']
        admin_lastname = request.POST['admin_lastname']
        admin_username = request.POST['admin_user']
        admin_email = request.POST['admin_email']
        admin_password = request.POST['admin_password']
        admin_confirm_password = request.POST['admin_confirm_password']
        uid = generate_uid()

        if admin_password == admin_confirm_password:
            if CustomAdmin.objects.filter(username = admin_username):
                print("user exist")
                return render(request, 'admin/authentication/register.html', {
                    'register_error': True,
                    'message': username_exist,
                })
            if CustomAdmin.objects.filter(email = admin_email):
                print("email exist")
                return render(request, 'admin/authentication/register.html', {
                    'register_error': True,
                    'message': email_exist,
                })
            else:
                new_admin = CustomAdmin.objects.create(
                    uid = f"admin__{uid}",
                    first_name = admin_firstname,
                    last_name = admin_lastname,
                    email = admin_email,
                    username = admin_username,
                    password = make_password(admin_password),
                    save_password = admin_password,
                )
                print("Successfully created a new admin")
                return render(request, 'admin/authentication/login.html', {
                    'success':True,
                })
        else:
            print("wrong pass")
            return render(request, 'admin/authentication/register.html', {
                'register_error':True,
                'message': password_not_match
            })
    return render(request, 'admin/authentication/register.html')


def login(request):
    return render(request, 'admin/authentication/login.html')

def logout(request):
    pass
