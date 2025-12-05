from django.urls import path
from .views import RegisterView, LoginView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name = "template/registration/register"),
    
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
   
]
