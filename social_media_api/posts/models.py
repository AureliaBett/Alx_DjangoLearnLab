from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL 


class Post(models.Model ):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,related_name='posts' ,on_delete=models.CASCADE)

   
    def __str__(self):
        return self.title
    
class Comment(models.Model ):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,related_name='comments' ,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='comments' ,on_delete=models.CASCADE)

   
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'