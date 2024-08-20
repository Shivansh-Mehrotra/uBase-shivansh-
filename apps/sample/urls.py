from django.contrib import admin
from django.urls import path

from apps.sample.views import QuestionsViewSet

urlpatterns = [
    path('questions', QuestionsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('questions/<int:pk>', QuestionsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        "patch": "partial_update",
        "delete": "soft_destroy"
    }))

]