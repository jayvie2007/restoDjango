from django.shortcuts import render

def index(request):
    return render(request, 'customer/index.html')


def food(request):
    return render(request, 'customer/menu/food.html')
def drink(request):
    return render(request, 'customer/menu/drink.html')
def side(request):
    return render(request, 'customer/menu/side.html')


def contact(request):
    return render(request, 'customer/contact.html')

def register(request):
    return render(request, 'customer/authentication/register.html')

def login(request):
    return render(request, 'customer/authentication/login.html')

