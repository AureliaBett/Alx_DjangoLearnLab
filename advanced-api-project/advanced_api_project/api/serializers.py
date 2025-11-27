from rest_framework import serializers
from .models import Book, Author



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields =['name']

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields ='__all__'

    def validate(self, data):
        if (data("publication_year")) > 2025:
            raise
        serializers.ValidationError("The year cannot be in the future")
        