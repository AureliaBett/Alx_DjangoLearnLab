from django.urls import path
from .import views

urlpatterns=[
    path('book_list/', views.book_list_view, name='book_list'),
    path('BookDetailView/', views.BookDetailView.as_view(), name='BookDetailView'),
]