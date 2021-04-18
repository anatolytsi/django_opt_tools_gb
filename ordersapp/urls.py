from django.urls import path

from ordersapp.views import OrderList, OrderCreate, OrderRead, OrderUpdate, OrderDelete, order_forming_complete, \
    get_product_price

app_name = 'ordersapp'

urlpatterns = [
    path("", OrderList.as_view(), name="index"),
    path("forming/complete/<int:pk>", order_forming_complete, name="order_forming_complete"),
    path("create/", OrderCreate.as_view(), name="order_create"),
    path("read/<int:pk>", OrderRead.as_view(), name="order_read"),
    path("update/<int:pk>", OrderUpdate.as_view(), name="order_update"),
    path("delete/<int:pk>", OrderDelete.as_view(), name="order_delete"),
    path('product/<int:pk>/price/', get_product_price, name="product_price")
]