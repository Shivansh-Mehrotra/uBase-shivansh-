from django.urls import path

from core.apps.lookup_management.views import LookupTypeViewSet, LookupViewSet

urlpatterns = [
    path('lookup-types/<pk>', LookupTypeViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update',
        'patch': 'partial_update',
        'get': 'retrieve'
    })),
    path('lookup-types', LookupTypeViewSet.as_view({'post': 'create', 'get': 'list'})),

    path('lookups/<pk>', LookupViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update' ,
        'patch': 'partial_update' ,
        'get': 'retrieve'
    })),
    path('lookups', LookupViewSet.as_view({'post': 'create', 'get': 'list'})),
]



