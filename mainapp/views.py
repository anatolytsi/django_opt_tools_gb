from django.core.paginator import Paginator
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
            "header": "GeekShop Store",
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
            "title": "GeekShop - Каталог",
            "categories": ProductCategory.objects.all()
        })
        if "category_id" in self.kwargs:
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
