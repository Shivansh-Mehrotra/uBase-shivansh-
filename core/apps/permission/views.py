from django.db.models import Q
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.apps.permission.models import Module, ModuleAction
from core.apps.permission.serializers import ModuleSerializers, ModuleActionSerializers, UserModuleActionSerializers
from core.permissions import IsSuperUser
from core.response import SimpleDataResponse
from core.viewsets import ModelViewSet
from core.permissions import StrictDjangoModelPermissions


class ModuleViewSet(ModelViewSet):
    queryset = Module.objects.filter(Q(parent__isnull=True) | Q(parent__is_deleted=False))
    serializer_class = ModuleSerializers

    set_ordering_fields = True
    ordering_fields_mapping = {
        'module_key': 'module_key',
        'label': 'label',
        'description': 'description',
        'order': 'order'
    }
    ordering_fields = list(ordering_fields_mapping.values())
    ordering = ('module_key',)
    search_fields = ['module_key', 'label']

    filterset_fields = ['is_active']
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]


class ModuleActionViewSet(ModelViewSet):
    queryset = ModuleAction.objects.all().select_related('module').prefetch_related('permissions')
    serializer_class = ModuleActionSerializers

    set_ordering_fields = True
    ordering_fields_mapping = {
        'action': 'action',
        'label': 'label',
        'description': 'description',
        'order': 'order'
    }
    ordering_fields = list(ordering_fields_mapping.values())
    ordering = ('action',)

    search_fields = [
        'action',
        'module__label',
        'module__app_source__source_key',
        'module__module_key'
    ]

    filterset_fields_mappings = {
        'module_label': 'module__label',
        'module_key': 'module__module_key',
        'app_source': 'module__app_source__source_key',
        'app_source_id': 'module__app_source_id',
    }
    filterset_fields = ['is_active', 'module', 'is_routable']
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]


class UserModuleActionViewSet(ModelViewSet):
    serializer_class = UserModuleActionSerializers
    set_request_user_tracking = True


class PermissionViewSet(APIView):
    # from rest_framework.decorators import api_view, permission_classes

    def _parse_actions(self, module_action):
        more_actions = []
        action_dict = {}
        for ma in module_action:
            action = {
                'id': ma.id, 'action': ma.action, 'label': ma.label,
                'description': ma.description, 'route_url': ma.route_url,
                'is_routable': ma.is_routable
            }
            key = None
            if ma.action.lower() in ('view', 'add', 'edit', 'delete'):
                key = ma.action.lower()

            if key:
                action_dict[key] = action
            else:
                more_actions.append(action)

        return action_dict, more_actions

    def get(self, request):
        data = []
        all_module = Module.objects.active().select_related('parent', 'app_source')\
            .prefetch_related('module_actions')

        app_source_id = request.query_params.get('app_source_id')
        app_source = request.query_params.get('app_source')
        if app_source_id:
            all_module = all_module.filter(app_source_id=app_source_id)
        if app_source:
            all_module = all_module.filter(app_source__source_key=app_source)

        for module in all_module:
            module_action = module.module_actions.all()
            actions, more = self._parse_actions(module_action)

            module_data = {
                'id': module.id,
                'label': module.label,
                'description': module.description,
                'key': module.module_key,
                'app_source': {
                    'label': module.app_source.label if module.app_source else None,
                    'key': module.app_source.source_key if module.app_source else None
                },
                'parent_id': module.parent_id,
                'parent_name': module.parent.module_key if module.parent else None,
                'actions': actions,
                'more': more
            }
            data.append(module_data)

        return SimpleDataResponse(data)

