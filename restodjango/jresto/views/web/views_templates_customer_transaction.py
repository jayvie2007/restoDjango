from django.shortcuts import render


def add_money(request):
    return render(request, 'money/add_money.html')
