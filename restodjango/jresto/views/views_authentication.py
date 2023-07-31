from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from jresto.models import CustomAdmin, CustomerDetails
from jresto.utils import *

from constants.status_code import *


def register(request):
    return render(request, 'product/authentication/register.html')

def login(request):
    return render(request, 'admin/authentication/login.html')

def logout(request):
    pass
