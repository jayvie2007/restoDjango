from django.shortcuts import render

from jresto.models import CustomerFeedback, Product
from jresto.utils import *

from constants.status_code import *


def index(request):
    total_cart_items = check_cart_function(request.user.id)
    wallet = get_wallet(request.user.id)
    return render(request, 'customer/index.html', {
        'cart_quantity': total_cart_items,
        'customer_cash': wallet,
    })


def menu(request):
    total_cart_items = check_cart_function(request.user.id)
    wallet = get_wallet(request.user.id)
    return render(request, 'customer/menu.html', {
        'cart_quantity': total_cart_items,
        'customer_cash': wallet,
    })


def food(request):
    total_cart_items = check_cart_function(request.user.id)
    wallet = get_wallet(request.user.id)
    products = Product.objects.filter(product_type="Meal")
    if request.user.is_authenticated == True and request.user.user_level == "Customer":
        add_order_item(request)
        return render(request, 'customer/menu/food.html', {
            'products': products,
            'cart_quantity': total_cart_items,
            'customer_cash': wallet,
        })

    return render(request, 'customer/menu/food.html', {
        'products': products,
        'cart_quantity': total_cart_items,
        'customer_cash': wallet,
    })


def drink(request):
    total_cart_items = check_cart_function(request.user.id)
    wallet = get_wallet(request.user.id)
    products = Product.objects.filter(product_type="Drink")
    if request.user.is_authenticated == True and request.user.user_level == "Customer":
        add_order_item(request)
        return render(request, 'customer/menu/drink.html', {
            'products': products,
            'cart_quantity': total_cart_items,
            'customer_cash': wallet,

        })

    return render(request, 'customer/menu/drink.html', {
        'products': products,
        'cart_quantity': total_cart_items,
        'customer_cash': wallet,
    })


def side(request):
    total_cart_items = check_cart_function(request.user.id)
    wallet = get_wallet(request.user.id)
    products = Product.objects.filter(product_type="Side")
    if request.user.is_authenticated == True and request.user.user_level == "Customer":
        add_order_item(request)
        return render(request, 'customer/menu/side.html', {
            'products': products,
            'cart_quantity': total_cart_items,
            'customer_cash': wallet,

        })

    return render(request, 'customer/menu/side.html', {
        'products': products,
        'cart_quantity': total_cart_items,
        'customer_cash': wallet,

    })


def contact(request):
    total_cart_items = check_cart_function(request.user.id)
    wallet = get_wallet(request.user.id)
    if request.method == 'POST':
        name = request.POST['feedback_name']
        email = request.POST['feedback_email']
        contact_number = request.POST['feedback_number']
        message = request.POST['feedback_message']

        CustomerFeedback.objects.create(
            name=name,
            email=email,
            contact_number=contact_number,
            message=message,
        )

        return render(request, 'customer/contact.html', {
            'message': message_success,
            'cart_quantity': total_cart_items,
            'customer_cash': wallet,
            'submit': True,
        })

    return render(request, 'customer/contact.html', {
        'cart_quantity': total_cart_items,
    })
