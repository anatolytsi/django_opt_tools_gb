import hashlib
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import ModelForm, DateInput

from authapp.models import User, UserProfile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        field = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Введите имя пользователя"
        self.fields["password"].widget.attrs["placeholder"] = "Введите пароль"
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control py-4"


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Введите имя пользователя"
        self.fields["email"].widget.attrs["placeholder"] = "Введите адрес эл. почты"
        self.fields["first_name"].widget.attrs["placeholder"] = "Введите имя"
        self.fields["last_name"].widget.attrs["placeholder"] = "Введите фамилию"
        self.fields["password1"].widget.attrs["placeholder"] = "Введите пароль"
        self.fields["password2"].widget.attrs["placeholder"] = "Подтвердите пароль"
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control py-4"

    def save(self, *args, **kwargs):
        user = super(UserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class UserProfileForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "avatar", "username", "email")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["readonly"] = True
        self.fields["email"].widget.attrs["readonly"] = True
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control py-4"
        self.fields["avatar"].widget.attrs["class"] = "custom-file-input"


class UserProfileEditForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ("tagline", "gender", "about_me", "birthday")
        widgets = {
            "birthday": DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
