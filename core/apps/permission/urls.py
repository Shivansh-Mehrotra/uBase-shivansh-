from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import *
# from django.conf.urls import url

app_name = 'login'

urlpatterns = [
    path('users/module-actions', UserModuleActionViewSet.as_view({'post': 'create'})),

    # path('role/module-action', RoleModuleActionViewSet.as_view({'post': 'create'})),

    path('modules/<pk>', ModuleViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update',
        'patch': 'partial_update',
        'get': 'retrieve'
    })),

    path('modules', ModuleViewSet.as_view({'post': 'create', 'get': 'list'})),

    path('module-actions/<pk>', ModuleActionViewSet.as_view({
        'delete': 'soft_destroy',
        'put': 'update' ,
        'patch': 'partial_update' ,
        'get': 'retrieve'
    })),
    path('module-actions', ModuleActionViewSet.as_view({'post': 'create', 'get': 'list'})),

    path('all', PermissionViewSet.as_view())

]



