from rest_framework.permissions import IsAuthenticated
from core.apps.role.models import Role, AppSource
from core.apps.role.serializers import RoleSerializers, AppSourceSerializers
from core.permissions import IsSuperUser, StrictDjangoModelPermissions
from core.viewsets import ModelViewSet
import json


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.filter(is_deleted=False)\
        .select_related('default_module_action', 'app_source').prefetch_related('module_actions')
    serializer_class = RoleSerializers
    set_request_user_tracking = True
    set_ordering_fields = True
    ordering_fields_mapping = {
        'name': 'name',
        'key': 'key',
        'module_action_name': 'module_action__action',
        'app_source': 'app_source__source_key'
    }
    ordering_fields = list(ordering_fields_mapping.values())
    ordering = ('-id',)

    search_fields = ('name', 'key', 'app_source__source_key',)

    filterset_fields_mappings = {
        'key': ('key', 'icontains'),
        'name': ('name', 'icontains'),
        'app_source': 'app_source__source_key',
        'app_source_id': 'app_source_id',
    }
    filterset_fields = ['is_active']
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]


class AppSourceViewSet(ModelViewSet):
    queryset = AppSource.objects.filter(is_deleted=False)
    serializer_class = AppSourceSerializers

    set_ordering_fields = True

    ordering_fields = ['source_key', 'label']
    ordering = ('-id',)

    search_fields = ('source_key', 'label')
    filterset_fields = ['source_key', 'label']

    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]

