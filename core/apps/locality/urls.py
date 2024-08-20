from django.urls import path

from core.apps.locality.views import CountryViewSet, StateViewSet, CityViewSet, LocalityViewSet

urlpatterns = [
    path('countries/<pk>', CountryViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update',
        'patch': 'partial_update',
        'get': 'retrieve'
    })),
    path('countries', CountryViewSet.as_view({'post': 'create', 'get': 'list'})),

    path('states/<pk>', StateViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update',
        'patch': 'partial_update',
        'get': 'retrieve'
    })),
    path('states', StateViewSet.as_view({'post': 'create', 'get': 'list'})),

    path('cities/<pk>', CityViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update',
        'patch': 'partial_update',
        'get': 'retrieve'
    })),
    path('cities', CityViewSet.as_view({'post': 'create', 'get': 'list'})),

    path('localities/<pk>', LocalityViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update',
        'patch': 'partial_update',
        'get': 'retrieve'
    })),
    path('localities', LocalityViewSet.as_view({'post': 'create', 'get': 'list'})),
]



