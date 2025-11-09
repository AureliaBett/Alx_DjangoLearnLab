from django.urls import path
from .import views
from .views import RegistrationView, LoginView, LogoutView, list_books, LibraryDetailView

urlpatterns=[
    path('', views.list_books, name='home'),
    path('list_books/', list_books, name='list_books'),
    path('LibraryDetailView/', LibraryDetailView.as_view(), name='LibraryDetailView'),
    
     path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
   
    
    
    ]