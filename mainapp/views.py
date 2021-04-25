from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from mainapp.models import Product, ProductCategory


# Create your views here.
# USER: functions = views = controllers


class ProductsIndexView(TemplateView):
    template_name = "mainapp/index.html"

    def get_context_data(self, **kwargs):
        context = super(ProductsIndexView, self).get_context_data()
        context.update({
            "title": "GeekShop",
            "description": "Новые образы и лучшие бренды на GeekShop Store.Бесплатная доставка по всему миру! Аутлет: до "
                           "-70% Собственный бренд. -20% новым покупателям. "
        })
        return context


class ProductsListView(ListView):
    template_name = "mainapp/products.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context.update({
            "title": "Каталог",
            "categories": ProductCategory.objects.all(),
            "category_id": 0
        })
        if "category_id" in self.kwargs and self.kwargs["category_id"] != 0:
            products = Product.objects.filter(category_id=self.kwargs["category_id"]).order_by("-price")
        else:
            products = Product.objects.all().order_by("-price")
        paginator = Paginator(products, per_page=3)
        if "page" in self.kwargs:
            products_paginator = paginator.page(self.kwargs["page"])
        else:
            products_paginator = paginator.page(1)
        context.update({"products": products_paginator})
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/products_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.all()


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products(request):
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


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
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True).order_by('price')


def products_ajax(request, pk=None, page=1):
    links_menu = get_links_menu()

    if pk:
        if pk == '0':
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = get_products_ordered_by_price()
        else:
            category = get_category(pk)
            products = get_products_in_category_ordered_by_price(pk)

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }

        result = render_to_string(
            'mainapp/products_list_inc.html',
            context=content,
            request=request)

        # return render(request, 'mainapp/products_list_inc.html', content)
        return JsonResponse({'result': result})


def category_choose(request, category_id=0, page=1):
    if request.is_ajax():
        # Hardcoded for now
        if 'detail' in request.headers['Referer']:
            return HttpResponse(reverse_lazy("mainapp:index"))
        if category_id == 0:
            products = Product.objects.all().order_by("-price")
        else:
            products = Product.objects.filter(category_id=category_id).order_by("-price")
        paginator = Paginator(products, per_page=3)
        products_paginator = paginator.page(page)
        content = ({
            "title": "Каталог",
            "categories": ProductCategory.objects.all(),
            "products": products_paginator,
            "category_id": category_id
        })
        result = render_to_string("mainapp/products_list_inc.html", context=content, request=request)
        return JsonResponse({"result": result})
