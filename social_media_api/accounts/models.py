from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, default='')
    email = models.EmailField(unique=True, default='')  
    password = models.CharField(max_length=128, default='')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    following = models.ManyToManyField('self', related_name='followers_set', symmetrical=False, blank=True)

   
    def __str__(self):
        return self.username
    
