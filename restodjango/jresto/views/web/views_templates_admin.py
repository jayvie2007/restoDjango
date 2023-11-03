from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from jresto.models import CustomerFeedback, Product, Order
from jresto.utils import *

from constants.status_code import *

import os


def admin_menu(request):
    if not request.user.user_level == "Admin":
        return redirect('index')

    return render(request, 'admin/menu.html')


def admin_add_menu(request):
    if not request.user.user_level == "Admin":
        return redirect('index')

    if request.method == "POST":
        try:
            product_image = request.FILES['product_image']
        except:
            product_image = None

        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_type = request.POST['product_type']
        product_description = request.POST['product_description']
        product_uid = generate_uid()

        if product_type == "Select Product Type":
            return render(request, 'admin/add_product.html', {
                'message': "Please select a product type",
                'success': False,
            })

        if product_type == "Meal":
            if product_name and Product.objects.filter(name=product_name, product_type=product_type).count() != 0:
                message = (
                    f"{product_name} is currently existing in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message': message,
                    'success': False,
                })
            else:
                # Handle image upload and linking
                if product_image:
                    # Check if the image already exists in MEDIA_ROOT
                    image_path = os.path.join(
                        settings.MEDIA_ROOT, product_image.name)
                    if not default_storage.exists(image_path):
                        # If the image doesn't exist, save it
                        default_storage.save(
                            image_path, ContentFile(product_image.read()))

                new_product = Product(
                    product_id=f"food__{product_uid}",
                    product_type=product_type,
                    name=product_name,
                    price=product_price,
                    description=product_description,
                    picture=product_image.name if product_image else None,
                )
                new_product.save()
                message = (
                    f"{product_name} has been added in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'success': True,
                    'message': message,
                })

        elif product_type == "Drink":
            if product_name and Product.objects.filter(name=product_name, product_type=product_type).count() != 0:
                message = (
                    f"{product_name} is currently existing in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message': message,
                    'success': False,
                })
            else:
                if product_image:
                    # Check if the image already exists in MEDIA_ROOT
                    image_path = os.path.join(
                        settings.MEDIA_ROOT, product_image.name)
                    if not default_storage.exists(image_path):
                        # If the image doesn't exist, save it
                        default_storage.save(
                            image_path, ContentFile(product_image.read()))

                new_products = Product(
                    product_id=f"drink__{product_uid}",
                    product_type=product_type,
                    name=product_name,
                    price=product_price,
                    description=product_description,
                    picture=product_image.name if product_image else None,
                )
                new_products.save()
                message = (
                    f"{product_name} has been added in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message': message,
                    'success': True,
                })

        elif product_type == "Side":
            if product_name and Product.objects.filter(name=product_name, product_type=product_type).count() != 0:
                message = (
                    f"{product_name} is currently existing in {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message': message,
                    'success': False,
                })
            else:
                if product_image:
                    # Check if the image already exists in MEDIA_ROOT
                    image_path = os.path.join(
                        settings.MEDIA_ROOT, product_image.name)
                    if not default_storage.exists(image_path):
                        # If the image doesn't exist, save it
                        default_storage.save(
                            image_path, ContentFile(product_image.read()))

                new_products = Product(
                    product_id=f"side__{product_uid}",
                    product_type=product_type,
                    name=product_name,
                    price=product_price,
                    description=product_description,
                    picture=product_image.name if product_image else None,
                )
                new_products.save()
                message = (
                    f"{product_name} has been added in type {product_type}")
                return render(request, 'admin/add_product.html', {
                    'message': message,
                    'success': True,
                })
        message = ("Please choose a product type!")
        return render(request, 'admin/add_product.html', {
            'message': message,
            'success': False
        })
    return render(request, 'admin/add_product.html')


def admin_display_menu(request):
    if not request.user.user_level == "Admin":
        return redirect('index')

    if request.method == 'POST':
        no_of_display = request.POST['no_of_display']
        product_filter = request.POST['product_filter']
        product_sort = request.POST['product_sort']

        # Check no of display for pagination
        if int(no_of_display) == 10:
            page_row = 10
        elif int(no_of_display) == 15:
            page_row = 15
        else:
            page_row = 5

        # Check product to be filtered
        if product_filter == "Meal":
            products = Product.objects.filter(product_type="Meal")
        elif product_filter == "Drink":
            products = Product.objects.filter(product_type="Drink")
        elif product_filter == "Side":
            products = Product.objects.filter(product_type="Side")
        else:
            products = Product.objects.all()

        # Check product sort to be sorted
        if product_sort == "Date Created":
            sort = "-date_created"
        elif product_sort == "Date Updated":
            sort = "-date_updated"
        elif product_sort == "Product Type":
            sort = "product_type"
        elif product_sort == "Name":
            sort = "name"
        else:
            sort = "-id"

    else:
        page_row = 5
        products = Product.objects.all()
        sort = "-id"

    pagination = Paginator(products.order_by(sort), page_row)
    page = request.GET.get('page')

    if page == None:
        product_list = pagination.get_page(page)
        page = 1
        return render(request, 'admin/display_product.html', {
            'product_list': product_list,
            'page_number': page
        })
    else:
        product_list = pagination.get_page(page)
        return render(request, 'admin/display_product.html', {
            'product_list': product_list,
            'page_number': int(page),
        })


def admin_edit_menu(request, product_id):
    try:
        products = Product.objects.get(product_id=product_id)
    except ObjectDoesNotExist:
        raise Http404("Product does not exist")
    if request.method == 'POST':
        try:
            product_image = request.FILES['product_image']
        except:
            product_image = None

        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_type = request.POST['product_type']
        product_description = request.POST['product_description']

        if products.picture:
            image_path = products.picture.path
            if default_storage.exists(image_path):
                default_storage.delete(image_path)
        if product_image:
            # Check if the image already exists in MEDIA_ROOT
            image_path = os.path.join(settings.MEDIA_ROOT, product_image.name)
            if not default_storage.exists(image_path):
                # If the image doesn't exist, save it
                default_storage.save(
                    image_path, ContentFile(product_image.read()))

        products.name = product_name
        products.price = product_price
        products.product_type = product_type
        products.description = product_description
        products.picture = product_image.name if product_image else None
        products.save()

        return render(request, 'admin/edit_product.html', {
            'products': products,
            'success': True,
            'message': "Successfully Edited!"
        })

    return render(request, 'admin/edit_product.html', {
        'products': products,
    })


def admin_delete_menu(request, product_id):
    try:
        products = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return HttpResponseRedirect(reverse('menu_product'))

    # Delete the associated image if it exists
    if products.picture:
        image_path = products.picture.path
        if default_storage.exists(image_path):
            default_storage.delete(image_path)
    products.delete()
    return HttpResponseRedirect(reverse('menu_product'))


def admin_feedback(request):
    if not request.user.user_level == "Admin":
        return redirect('index')

    if request.method == 'POST':
        no_of_display = request.POST['no_of_display']
        sort_by = request.POST['feedback_sort']
        search_word = request.POST['feedback_search']
        category = request.POST['feedback_category']

        if int(no_of_display) == 10:
            page_row = 10
        elif int(no_of_display) == 15:
            page_row = 15
        else:
            page_row = 5

        if sort_by == "Name":
            sort = "name"
        elif sort_by == "Email":
            sort = "email"
        elif sort_by == "Date Created":
            sort = "-date_created"
        else:
            sort = "-id"

        if len(search_word):
            if category == "Name":
                feedbacks = CustomerFeedback.objects.filter(
                    name__icontains=search_word)
            elif category == "Email":
                feedbacks = CustomerFeedback.objects.filter(
                    email__icontains=search_word)
            else:
                feedbacks = CustomerFeedback.objects.filter(
                    Q(name__icontains=search_word) | Q(email__icontains=search_word))
        else:
            feedbacks = CustomerFeedback.objects.all()
    else:
        page_row = 5
        feedbacks = CustomerFeedback.objects.all()
        sort = "-id"

    pagination = Paginator(feedbacks.order_by(sort), page_row)
    page = request.GET.get('page')
    if page == None:
        feedback_list = pagination.get_page(page)
        page = 1
        return render(request, 'admin/check_feedback.html', {
            'feedback_list': feedback_list,
            'page_number': page,
        })
    else:
        feedback_list = pagination.get_page(page)
        return render(request, 'admin/check_feedback.html', {
            'feedback_list': feedback_list,
            'page_number': int(page),
        })


def admin_feedback_delete(request, id):
    feedbacks = CustomerFeedback.objects.get(id=id)
    feedbacks.delete()
    return HttpResponseRedirect(reverse('admin_feedback'))


def admin_transaction(request):
    print(request.user.is_authenticated, request.user.user_level)
    if request.user.is_authenticated == True and request.user.user_level == "Admin":
        orders = Order.objects.all()

    return render(request, 'admin/check_transactions.html', {
        'orders': orders,
    })


def admin_transaction_list(request, id):
    return render(request, 'admin/check_transactions_list.html')
