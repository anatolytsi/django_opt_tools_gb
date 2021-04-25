import hashlib
import random

from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db import transaction

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from django.views.generic import FormView, UpdateView

from .models import User


class GeekLoginView(FormView):
    model = User
    success_url = reverse_lazy("index")
    form_class = UserLoginForm
    template_name = "authapp/login.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            usr = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")

            user = authenticate(username=usr, password=pwd)

            if user and user.is_active:
                login(request, user)
                return redirect(self.success_url)

        return render(request, self.template_name, {"form": form})


class RegisterView(FormView):
    model = User
    form_class = UserRegisterForm
    template_name = "authapp/register.html"
    success_url = reverse_lazy("authapp:login")

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save()
            if self.send_verify_mail(user):
                messages.success(request, "Вы успешно зарегистрировались!<br/>"
                                          "Письмо со ссылкой для активации акаунта выслано на почту")

            return redirect(self.success_url)

        return render(request, self.template_name, {"form": form})

    def verify(self, email, activation_key):
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(self, user, backend="django.contrib.auth.backends.ModelBackend")
            return render(self, "authapp/verification.html")
        else:
            print(f"Error activating user: {user}")
            return render(self, "authapp/verification.html")

    @staticmethod
    def send_verify_mail(user):
        verify_link = reverse_lazy("authapp:verify", args=[user.email, user.activation_key])

        title = f"Активация учетной записи {user.username}"

        message = f"Для подтверждения учетной записи {user.username} пройдите по ссылке: \n{settings.DOMAIN_NAME}" \
                  f"{verify_link}"

        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email, ], fail_silently=False)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    second_form_class = UserProfileEditForm
    template_name = "authapp/profile.html"
    success_url = reverse_lazy("auth:profile")

    def get(self, *args, **kwargs):
        if self.request.user.pk:
            return super(ProfileView, self).get(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("auth:login"))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if "profile_form" not in context:
            context["profile_form"] = self.second_form_class(instance=self.request.user.userprofile)
        context.update({
            "title": "GeekShop - Профиль",
        })
        return context

    @transaction.atomic
    def form_valid(self, form, *args, **kwargs):
        profile_form = UserProfileEditForm(
            data=self.request.POST,
            files=self.request.FILES,
            instance=self.request.user.userprofile
        )
        if profile_form.is_valid():
            form.save()
            profile_form.save()
            return HttpResponseRedirect(self.success_url)
        return render(self.request, self.template_name, {"form": form, "profile_form": profile_form})

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)
