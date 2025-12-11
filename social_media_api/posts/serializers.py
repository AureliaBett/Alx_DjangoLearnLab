from rest_framework import serializers
from django.conf import settings
from .models import Post, Comment

User = settings.AUTH_USER_MODEL

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author']
        


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'author', 'post']


