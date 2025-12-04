from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="authors")

