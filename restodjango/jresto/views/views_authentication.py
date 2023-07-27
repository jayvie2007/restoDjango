from django.shortcuts import render

def register(request):
    return render(request, 'register/register.html')

def login(request):
    return render(request, 'login/login.html')

def logout(request):
    pass
