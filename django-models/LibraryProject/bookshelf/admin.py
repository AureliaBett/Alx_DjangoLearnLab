from django.contrib import admin
from .models import Book

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

