from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Metta:
        model = Book
        fields = "__all__"

