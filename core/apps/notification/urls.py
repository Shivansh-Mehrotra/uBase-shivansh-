# from django.conf.urls import url
from django.urls import path
# from apps.ubase.notification.views import Notification
from core.apps.notification.views import Notification

app_name = 'notification'

urlpatterns = [
    path('email/', Notification.as_view({'post': 'email_notification'}))
]
