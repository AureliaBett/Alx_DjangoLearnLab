from django.urls import path
from .import views
from .views import register, LoginView, LogoutView, LibraryDetailView
from .views import list_books
urlpatterns=[
    path('', views.list_books, name='home'),
    path('list_books/', list_books, name='list_books'),
    path('LibraryDetailView/', LibraryDetailView.as_view(), name='LibraryDetailView'),
    
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
   
    path('admin_dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian_dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member_dashboard/', views.member_view, name='member_dashboard'),
    

    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),
    ]