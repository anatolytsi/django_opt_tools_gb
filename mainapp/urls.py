from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp.views import ProductsListView, get_products, products_ajax, category_choose, ProductDetail

app_name = 'mainapp'

urlpatterns = [
    path("", cache_page(3600)(ProductsListView.as_view()), name='index'),
    # path("category/<int:pk>/ajax/", cache_page(3600)(products_ajax), name='ajax'),
    path("<int:category_id>/", cache_page(3600)(ProductsListView.as_view()), name="category"),
    path("page/<int:page>/", cache_page(3600)(ProductsListView.as_view()), name="page"),
    path("category/<int:category_id>/page/<int:page>/", category_choose, name="category_choose"),
    path('detail/<int:pk>/', ProductDetail.as_view(), name="detail"),
]
