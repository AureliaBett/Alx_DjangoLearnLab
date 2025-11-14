
import os
import sys
import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Setup Django environment ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# --- Import models ---
from relationship_app.models import Author, Book, Library, Librarian


# --- Query 1: All books by a specific author ---
author_name = "Jane Smith"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"\n📚 Books by {author_name}:")
    if books_by_author.exists():
        for book in books_by_author:
            print(f"- {book.title}")
    else:
        print("No books found for this author.")
except Author.DoesNotExist:
    print(f"\n⚠️ Author '{author_name}' not found.")


# --- Query 2: List all books in a specific library ---
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"\n🏛️ Books in {library.name}:")
    if books_in_library.exists():
        for book in books_in_library:
            print(f"- {book.title}")
    else:
        print("No books found in this library.")
except Library.DoesNotExist:
    print(f"\n⚠️ Library named '{library_name}' not found.")


# --- Query 3: Retrieve the librarian for a specific library ---
try:
    librarian = Librarian.objects.get(library=library)
    print(f"\n👩‍💼 Librarian for {library_name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"\n⚠️ No librarian found for '{library_name}'.")