from django.forms import ModelForm

from ordersapp.models import Order, OrderItem


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"