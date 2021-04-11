from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from basketapp.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderList(LoginRequiredMixin, ListView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        context["title"] = "GeekShop - Заказы"
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    context_object_name = "object"
    success_url = reverse_lazy("orders:index")

    def get_context_data(self, **kwargs):
        data = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial["product"] = basket_items[num].product
                    form.initial["quantity"] = basket_items[num].quantity
                    form.initial["price"] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()
        data["orderitems"] = formset
        data["title"] = "Новый заказ"
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy("orders:index")

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            context["orderitems"] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            context["orderitems"] = OrderFormSet(instance=self.object)
            for form in context["orderitems"]:
                if form.instance.pk:
                    form.initial["price"] = form.instance.product.price

        context["title"] = "Редактирование заказа"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy("orders:index")

    def get_context_data(self, **kwargs):
        context = super(OrderDelete, self).get_context_data(**kwargs)
        context["title"] = "Удаление заказа"
        return context


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context["title"] = "Просмотр заказа"
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse("orders:index"))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields == "quantity" or "product":
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
