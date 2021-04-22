from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
import os

from mainapp.models import Product, ProductsCategory

dir = os.path.dirname(__file__)


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):
    slides = os.listdir(os.path.join(settings.STATIC_URL[1:],
                                     'vendor/img/slides/'))

    context = {'title': 'GeekShop - каталог',
               'slides': slides,
               'categories': get_links_menu(),
               }
    if category_id:
        products_list = Product.objects.filter(
            category_id=category_id).order_by('price')
    else:
        products_list = Product.objects.all().order_by('price')
    paginator = Paginator(products_list, 3)
    products_paginator = paginator.page(page)
    context.update({'products': products_paginator})
    return render(request, 'mainapp/products.html', context)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductsCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductsCategory.objects.all()


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductsCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductsCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).select_related(
                'category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True,
                                      category__is_active=True).select_related(
            'category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(
                category_id=category_id).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(
                category_id=category_id).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk).order_by('price')
