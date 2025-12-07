from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, post_search, posts_by_tag
)
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="registration/logout_out.html"), name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path('post/', PostListView.as_view(), name='post-list'),                   # List all posts
    path('post/new/', PostCreateView.as_view(), name='post-create'),           # Create a new post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),      # View post details
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # Update a post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # Delete a post
    path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:pk>/comments/new/', PostDetailView.as_view(), name='post-detail'),
    path('comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', post_search, name='post-search'),
    path('tags/<str:tag_name>/', posts_by_tag, name='posts-by-tag'),

]
