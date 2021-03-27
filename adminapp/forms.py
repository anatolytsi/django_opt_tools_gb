from django import forms

from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User
from mainapp.models import Product, ProductCategory


class UserAdminRegisterForm(UserRegisterForm):
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ("username", "email", "avatar", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields["avatar"].widget.attrs["class"] = "custom-file-input"


class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["readonly"] = False
        self.fields["email"].widget.attrs["readonly"] = False


class ProductAdminForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Product
        fields = ("name", "description", "short_description", "price", "quantity", "image", "category")
        
    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control py-4"
        self.fields["image"].widget.attrs["class"] = "custom-file-input"


class ProductCategoryAdminForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super(ProductCategoryAdminForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control py-4"

