from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import path
from django.contrib.auth.views import LogoutView


# Create your views here.
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library


def list_books(request):
    books= Book.objects.all()
    context = {'list_books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context

#User Registration
class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

    # (Optional) Automatically log in the user after registration
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # <-- using the imported login
        return super().form_valid(form)
#User Login
urlpatterns = [
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'relationship_app/login.html'), name='logout'),
]