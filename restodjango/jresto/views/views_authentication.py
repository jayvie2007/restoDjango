from django.shortcuts import render

def register(request):
    return render(request, 'admin/authentication/register.html')

def login(request):
    return render(request, 'admin/authentication/login.html')

def logout(request):
    pass
