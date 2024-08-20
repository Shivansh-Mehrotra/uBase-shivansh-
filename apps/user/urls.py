from django.contrib import admin
from django.urls import path

from apps.user.views import UsersViewSet, UserProfileViewSet

urlpatterns = [
    path('users', UsersViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('users/<int:pk>', UsersViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        "patch": "partial_update",
        "delete": "soft_destroy"
    })),

    path('user/profile', UserProfileViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    }))

]