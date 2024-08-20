from django.urls import path
from .views import RoleViewSet, AppSourceViewSet

app_name = 'role'

urlpatterns = [
    path('roles/<pk>', RoleViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update',
        'patch': 'partial_update',
        'get': 'retrieve'
    })),
    path('roles', RoleViewSet.as_view({'post': 'create', 'get': 'list'})),

    path('app-sources/<pk>', AppSourceViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update',
        'get': 'retrieve'
    })),
    path('app-source', AppSourceViewSet.as_view({'post': 'create', 'get': 'list'}))
]
