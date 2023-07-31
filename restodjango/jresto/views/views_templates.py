from django.shortcuts import render

def index(request):
    return render(request, 'product/index.html')


def menu(request):
    return render(request, 'product/menu.html')


def contact(request):
    return render(request, 'product/contact.html')

def register(request):
    return render(request, 'customer/register.html')

def login(request):
    return render(request, 'customer/login.html')

