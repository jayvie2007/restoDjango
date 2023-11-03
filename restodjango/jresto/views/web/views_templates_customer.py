from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse

from datetime import date

from jresto.models import CustomUser, OrderItem, Order, DeliveryInfo, Customer
from jresto.utils import *

from constants.status_code import *


def check_cart(request):
    try:
        customer_id = request.user.id
        customer = CustomUser.objects.get(id=customer_id)
    except:
        return redirect('user_login')

    orders = Order.objects.filter(customer=customer, complete=False)
    orderitems = OrderItem.objects.filter(
        order__customer=customer, order__complete=False)
    total_cart_value = sum(order.get_cart_total for order in orders)
    total_cart_items = orders.aggregate(Sum('orderitem__quantity'))[
        'orderitem__quantity__sum']

    return render(request, 'order/cart.html', {
        'orderitems': orderitems,
        'total_cart_value': total_cart_value,
        'cart_quantity': total_cart_items,

    })


def update_cart(request, name):
    try:
        customer_id = request.user.id
        customer = CustomUser.objects.get(id=customer_id)
    except:
        return redirect('user_login')
    try:
        orderitems = OrderItem.objects.get(
            order__customer=customer, order__complete=False, product__name=name)
    except:
        return redirect('check_cart')

    orders = Order.objects.filter(customer=customer, complete=False)
    total_cart_items = orders.aggregate(Sum('orderitem__quantity'))[
        'orderitem__quantity__sum']

    if request.method == 'POST':
        product_quantity = request.POST['product_quantity']
        if product_quantity == '0':
            orderitems.delete()
            return HttpResponseRedirect(reverse('check_cart'))
        else:
            orderitems.quantity = product_quantity
            orderitems.save()
            return render(request, 'order/update_cart.html', {
                'orderitems': orderitems,
                'success': True,
                'message': "Changes has been saved",
                'cart_quantity': total_cart_items,
            })
    return render(request, 'order/update_cart.html', {
        'orderitems': orderitems,
        'cart_quantity': total_cart_items,

    })


def remove_cart(request, name):
    try:
        customer_id = request.user.id
        customer = CustomUser.objects.get(id=customer_id)
    except:
        return redirect('user_login')
    try:
        orderitems = OrderItem.objects.get(
            order__customer=customer, order__complete=False, product__name=name)
    except:
        return redirect('check_cart')
    orderitems.delete()
    return HttpResponseRedirect(reverse('checkout'))


def checkout(request):
    try:
        customer_id = request.user.id
        customer = CustomUser.objects.get(id=customer_id)
    except:
        return redirect('user_login')

    orders = Order.objects.filter(customer=customer, complete=False)
    total_cart_items = orders.aggregate(Sum('orderitem__quantity'))[
        'orderitem__quantity__sum']

    wallet = Customer.objects.get(customer_id=customer_id)
    orderitems = OrderItem.objects.filter(
        order__customer=customer, order__complete=False)
    total_cart_value = sum(order.get_cart_total for order in orders)
    shipping_fee = total_cart_value * .05
    overall_total = total_cart_value + shipping_fee
    remaining_balance = wallet.cash - overall_total

    if request.method == "POST":
        delivery_first_name = request.POST['delivery_first_name']
        delivery_last_name = request.POST['delivery_last_name']
        delivery_address = request.POST['delivery_address']
        delivery_province = request.POST['delivery_province']
        delivery_city = request.POST['delivery_city']
        delivery_barangay = request.POST['delivery_barangay']
        delivery_zip_code = request.POST['delivery_zip_code']
        contact_email = request.POST['contact_email']
        contact_number = request.POST['contact_number']

        if remaining_balance < 0:
            return render(request, 'order/checkout.html', {
                'orderitems': orderitems,
                'total_cart_value': total_cart_value,
                'shipping_fee': shipping_fee,
                'overall_total': overall_total,
                'wallet': wallet,
                'remaining_balance': remaining_balance,
                'success': False,
                'cart_quantity': total_cart_items,
            })
        else:
            delivery_info = DeliveryInfo(
                first_name=delivery_first_name,
                last_name=delivery_last_name,
                address=delivery_address,
                province=delivery_province,
                city=delivery_city,
                barangay=delivery_barangay,
                zip_code=delivery_zip_code,
                email=contact_email,
                contact_number=contact_number,
            )
            wallet.cash = remaining_balance
            wallet.save()
            delivery_info.save()

            for order in orders:
                order.complete = True
                order.status = "Completed"
                order.total_bill = overall_total
                order.transaction_id = f"{generate_uid()}__" + \
                    str(date.today())
                order.date_completed = date.today()
                order.save()

            for orderitem in orderitems:
                orderitem.date_complete = date.today()
                orderitem.save()

            return render(request, 'order/checkout.html', {
                'orderitems': orderitems,
                'total_cart_value': 0,
                'shipping_fee': 0,
                'overall_total': 0,
                'wallet': wallet,
                'remaining_balance': remaining_balance,
                'cart_quantity': total_cart_items,
                'success': True,
            })

    return render(request, 'order/checkout.html', {
        'orderitems': orderitems,
        'total_cart_value': total_cart_value,
        'shipping_fee': shipping_fee,
        'overall_total': overall_total,
        'wallet': wallet,
        'remaining_balance': remaining_balance,
        'cart_quantity': total_cart_items,
        'success': "",
    })
