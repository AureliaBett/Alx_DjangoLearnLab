from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

   
    permission_classes = [IsAuthenticated]

   
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
