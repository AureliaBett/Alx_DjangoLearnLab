from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from api.models import Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Authenticate the client
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        # Create sample books
        self.book1 = Book.objects.create(
            title="A Tale of Two Cities",
            author="Charles Dickens",
            published_year=1859
        )
        self.book2 = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            published_year=1925
        )

        # Store URLs
        self.list_url = reverse("book-list")
        self.detail_url = lambda pk: reverse("book-detail", args=[pk])
        self.create_url = reverse("book-create")
        self.update_url = lambda pk: reverse("book-update", args=[pk])
        self.delete_url = lambda pk: reverse("book-delete", args=[pk])

    
    # LIST / GET TEST
    
    def test_list_books(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

  
    # CREATE TEST

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "Author Name",
            "published_year": 2024
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "New Book")

    # RETRIEVE ONE BOOK

    def test_get_single_book(self):
        response = self.client.get(self.detail_url(self.book1.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "A Tale of Two Cities")

 
    # UPDATE TEST

    def test_update_book(self):
        data = {"title": "Updated Title"}

        response = self.client.patch(self.detail_url(self.book1.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

   
    # DELETE TEST
    
    def test_delete_book(self):
        response = self.client.delete(self.detail_url(self.book1.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())


    # FILTERING TEST

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {"author": "F. Scott Fitzgerald"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "The Great Gatsby")

    
    # SEARCH TEST
    
    def test_search_books(self):
        response = self.client.get(self.list_url, {"search": "Cities"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Charles Dickens")

    
    # ORDERING TEST
    
    def test_order_books_by_year(self):
        response = self.client.get(self.list_url, {"ordering": "published_year"})

        years = [book["published_year"] for book in response.data]

        self.assertEqual(years, sorted(years))

    
    # AUTH REQUIRED TEST
    
    def test_authentication_required_for_create(self):
        client = APIClient()  # unauthenticated

        response = client.post(self.list_url, {
            "title": "Fail Book",
            "author": "None",
            "published_year": 2000
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
