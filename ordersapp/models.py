from django.conf import settings
from django.db import models
from django.utils import timezone

from mainapp.models import Product


class Order(models.Model):
    FORMING = "FM"
    SENT_TO_PROCEED = "STP"
    PAID = "PD"
    PROCEEDED = "PRD"
    READY = "RDY"
    CANCEL = "CNC"

    ORDER_STATUS_CHOICES = (
        (FORMING, "формируется"),
        (SENT_TO_PROCEED, "отправлен в обработку"),
        (PAID, "оплачен"),
        (PROCEEDED, "обрабатывается"),
        (READY, "готов к выдаче"),
        (CANCEL, "отменен"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="создан", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="обновлен", auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name="статус", max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name="активен", default=True, db_index=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Текущий заказ {self.id}"

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    # def get_total_quantity(self):
    #     items = self.orderitems.select_related()
    #     return sum(list(map(lambda x: x.quantity, items)))
    #
    # def get_product_quantity(self):
    #     items = self.orderitems.select_related()
    #     return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="продукт", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="количество", default=0)

    class Meta:
        verbose_name = "продукты заказа"
        verbose_name_plural = "продукты заказов"

    def get_product_cost(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        self.order.updated = timezone.now()
        super(OrderItem, self).save(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super(OrderItem, self).delete(*args, **kwargs)
