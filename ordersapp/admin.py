from django.contrib import admin

from mainapp.models import ProductCategory, Product
from ordersapp.models import OrderItem, Order

admin.site.register(Order)
admin.site.register(OrderItem)

# @admin.register(OrderItem)
# class OrderItemsAdmin(admin.ModelAdmin):
#     list_display = ("user", "price", "quantity", "category")
#     fields = ("name", "image", "description", "short_description", ("price", "quantity"), "category")
#     readonly_fields = ("short_description",)
#     ordering = ("name",)
#     search_fields = ("name",)
#
#
# @admin.register(ProductCategory)
# class ProductCategoryAdmin(admin.ModelAdmin):
#     list_display = ("name",)
#     fields = ("name", "description")
#     readonly_fields = ("name",)
#     ordering = ("name",)
#     search_fields = ("name",)
