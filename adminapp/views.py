from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from authapp.models import User
from mainapp.models import Product, ProductCategory
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductAdminForm, ProductCategoryAdminForm


class AdminIndexView(TemplateView):
    template_name = "adminapp/index.html"

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminIndexView, self).dispatch(request, *args, **kwargs)


# READ
class UserListView(ListView):
    model = User
    template_name = "adminapp/admin-users-read.html"

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


# CREATE
class UserCreateView(CreateView):
    model = User
    template_name = "adminapp/admin-users-create.html"
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy("admin_staff:admin_users")

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


# UPDATE
class UserUpdateView(UpdateView):
    model = User
    template_name = "adminapp/admin-users-update-delete.html"
    form_class = UserAdminProfileForm
    success_url = reverse_lazy("admin_staff:admin_users")

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context["title"] = "GeekShop - Редактирование пользователя"
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


# DELETE
class UserDeleteView(DeleteView):
    model = User
    template_name = "adminapp/admin-users-update-delete.html"
    success_url = reverse_lazy("admin_staff:admin_users")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


# READ
class ProductListView(ListView):
    model = Product
    template_name = "adminapp/admin-products-read.html"

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)


# CREATE
class ProductCreateView(CreateView):
    model = Product
    template_name = "adminapp/admin-products-create.html"
    form_class = ProductAdminForm
    success_url = reverse_lazy("admin_staff:admin_products")

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(request, *args, **kwargs)


# UPDATE
class ProductUpdateView(UpdateView):
    model = Product
    template_name = "adminapp/admin-products-update-delete.html"
    form_class = ProductAdminForm
    success_url = reverse_lazy("admin_staff:admin_products")

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        context["title"] = "GeekShop - Редактирование товара"
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)


# DELETE
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "adminapp/admin-products-update-delete.html"
    success_url = reverse_lazy("admin_staff:admin_products")

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)


# READ
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = "adminapp/admin-categories-read.html"

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCategoryListView, self).dispatch(request, *args, **kwargs)


# CREATE
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = "adminapp/admin-categories-create.html"
    form_class = ProductCategoryAdminForm
    success_url = reverse_lazy("admin_staff:admin_categories")

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCategoryCreateView, self).dispatch(request, *args, **kwargs)


# UPDATE
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = "adminapp/admin-categories-update-delete.html"
    form_class = ProductCategoryAdminForm
    success_url = reverse_lazy("admin_staff:admin_categories")

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data()
        context["title"] = "GeekShop - Редактирование категорий"
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCategoryUpdateView, self).dispatch(request, *args, **kwargs)


# DELETE
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = "adminapp/admin-categories-update-delete.html"
    success_url = reverse_lazy("admin_staff:admin_categories")

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCategoryDeleteView, self).dispatch(request, *args, **kwargs)
