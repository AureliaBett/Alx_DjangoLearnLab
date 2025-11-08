from django.shortcuts import render


# Create your views here.
from django.views.generic import DetailView
from .models import Book


def book_list(request):
    books= Book.objects.all()
    context = {'book_list': books}
    return(request, 'relationship_app/list_books', context)

class BookDetailView(DetailView):
    model = Book
    template_name = 'relationship_app/list_books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context