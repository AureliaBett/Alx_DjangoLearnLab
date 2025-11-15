from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm


# List Books
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()  # ORM protects from SQL injection
    return render(request, 'bookshelf/book_list.html', {'books': books})


# Create Book (Secure)
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)

        if form.is_valid():         # Validates + sanitizes input
            form.save()
            return redirect('book_list')

    else:
        form = ExampleForm()

    return render(request, 'bookshelf/book_form.html', {'form': form})


# Edit Book (Secure)
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect('book_list')

    else:
        form = BookForm(instance=book)

    return render(request, 'bookshelf/book_form.html', {'form': form})


# Delete Book (Secure)
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":  # Prevent accidental deletes via GET
        book.delete()
        return redirect('book_list')

    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
