from django.shortcuts import render

from jresto.models import CustomerFeedback
from constants.status_code import *

def index(request):
    return render(request, 'customer/index.html')

def food(request):
    return render(request, 'customer/menu/food.html')
def drink(request):
    return render(request, 'customer/menu/drink.html')
def side(request):
    return render(request, 'customer/menu/side.html')

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
        })
    return render(request, 'customer/contact.html')

def register(request):
    return render(request, 'customer/authentication/register.html')

def login(request):
    return render(request, 'customer/authentication/login.html')

