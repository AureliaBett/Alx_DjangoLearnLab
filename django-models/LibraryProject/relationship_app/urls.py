from django.urls import path
from .import views
from .views import list_books

urlpatterns=[
    path('list_books/', views.book_list, name='list_books'),
    path('LibraryDetailView/', views.LibraryDetailView.as_view(), name='LibraryDetailView'),
]