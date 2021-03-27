from django.contrib import admin

from authapp.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "is_active")
    fields = ("username", ("first_name", "last_name"), "email", "avatar", "groups", ("is_active", "is_superuser", "is_staff"), "last_login", "date_joined")
    readonly_fields = ("last_login", "date_joined", )
    ordering = ("username",)
    search_fields = ("first_name", "last_name", "username")
