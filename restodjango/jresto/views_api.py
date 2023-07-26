from django.shortcuts import render

def index(request):
    return render(request, 'dashboard/dashboard.html')

def menu_add_food(request):
    pass
def menu_add_drink(request):
    pass
def menu_add_side(request):
    pass
