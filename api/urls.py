from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'friend-requests', views.FriendRequestViewSet, basename='friend-request')
router.register(r'chats', views.ChatViewSet, basename='chat')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
