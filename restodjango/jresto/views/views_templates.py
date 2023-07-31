from django.shortcuts import render

def index(request):
    return render(request, 'admin/authentication/register.html')

