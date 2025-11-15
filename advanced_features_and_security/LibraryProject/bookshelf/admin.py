from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from django import forms
from .models import CustomUser

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # columns to show in the changelist
    list_display = ("id", "title", "author", "publication_year")
    # fields that can be edited directly in the changelist (optional)
    list_editable = ("publication_year",)
    # quick filters in the right sidebar
    list_filter = ("publication_year", "author")
    # fields to search by using the search box
    search_fields = ("title", "author")
    # default ordering
    ordering = ("-publication_year", "title")
    # number of items per page in changelist
    list_per_page = 25
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
        widgets = {
            "email": TextInput(attrs={"size": 40}),
            "first_name": TextInput(attrs={"size": 40}),
            "last_name": TextInput(attrs={"size": 40}),
        }

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm

    # Fields shown in the list view
    list_display = ("email", "first_name", "last_name", "date_of_birth", "is_staff")

    # Filtering options in admin sidebar
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Fields shown when editing a user
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "profile_photo",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField()
    profile_photo = models.ImageField()