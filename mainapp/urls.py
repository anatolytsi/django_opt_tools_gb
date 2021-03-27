from django.urls import path

from mainapp.views import ProductsListView

app_name = 'mainapp'

urlpatterns = [
    path("", ProductsListView.as_view(), name='index'),
    path("<int:category_id>/", ProductsListView.as_view(), name="category"),
    path("page/<int:page>/", ProductsListView.as_view(), name="page"),
    path("product/<int:pk>/", ProductsListView.as_view(), name="product"),
]
