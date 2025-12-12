from django.urls import path
from .views import NotificationListView

urlpatterns = [
    path('/notafications', NotificationListView.as_view(), name='notification-list'),
]
