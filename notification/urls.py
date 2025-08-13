from django.urls import path
from notification.views import ShowNotifications, mark_notification_read, mark_all_notifications_read, get_unread_count

urlpatterns = [
    path('', ShowNotifications, name='show-notifications'),
    path('mark-read/', mark_notification_read, name='mark-notification-read'),
    path('mark-all-read/', mark_all_notifications_read, name='mark-all-notifications-read'),
    path('unread-count/', get_unread_count, name='get-unread-count'),
]