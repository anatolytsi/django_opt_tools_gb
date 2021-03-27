from django.urls import path

from adminapp.views import (AdminIndexView, UserListView, UserCreateView, UserUpdateView, UserDeleteView)
from adminapp.views import (ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView)
from adminapp.views import (ProductCategoryListView, ProductCategoryCreateView, ProductCategoryUpdateView, ProductCategoryDeleteView)

app_name = 'adminapp'

urlpatterns = [
    path("", AdminIndexView.as_view(), name="index"),
    path("users/", UserListView.as_view(), name="admin_users"),
    path("users-create/", UserCreateView.as_view(), name="admin_users_create"),
    path("users-update/<int:pk>/", UserUpdateView.as_view(), name="admin_users_update"),
    path("users-delete/<int:pk>/", UserDeleteView.as_view(), name="admin_users_delete"),
    path("products/", ProductListView.as_view(), name="admin_products"),
    path("products-create/", ProductCreateView.as_view(), name="admin_products_create"),
    path("products-update/<int:pk>/", ProductUpdateView.as_view(), name="admin_products_update"),
    path("products-delete/<int:pk>/", ProductDeleteView.as_view(), name="admin_products_delete"),
    path("categories/", ProductCategoryListView.as_view(), name="admin_categories"),
    path("categories-create/", ProductCategoryCreateView.as_view(), name="admin_categories_create"),
    path("categories-update/<int:pk>/", ProductCategoryUpdateView.as_view(), name="admin_categories_update"),
    path("categories-delete/<int:pk>/", ProductCategoryDeleteView.as_view(), name="admin_categories_delete"),
]
