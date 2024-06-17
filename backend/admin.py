from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from backend.models.user import User
from django.apps import apps

# Register your models here.
app_config = apps.get_app_config("backend")


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "name", "role", "user_type", "status", "is_active", )
    list_filter = ("user_type", "is_active", "role", "status")
    fieldsets = (
        (None, {"fields": ("email", "user_type", "status")}),
        ("Personal info", {"fields": ("name", "mobile", "profile_pic")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Time Stamps", {"fields": ("last_login", "date_joined", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password", "confirm_password", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email", "name")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)

for model in app_config.get_models():
    if model != User:
        admin.site.register(model)
