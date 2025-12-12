from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL 


class Notification(models.Model):
    
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name='actor_notifications', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_post = models.ForeignKey('posts.Post', related_name='post_notifications', null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)