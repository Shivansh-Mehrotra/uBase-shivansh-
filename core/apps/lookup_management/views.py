from django.db.models import Q

from rest_framework.permissions import IsAuthenticated

from core.apps.lookup_management.models import LookupType, Lookup
from core.apps.lookup_management.serializers import LookupTypeSerializer, LookupSerializer
from core.viewsets import ModelViewSet
from core.permissions import StrictDjangoModelPermissions


class LookupTypeViewSet(ModelViewSet):
    queryset = LookupType.objects.filter(is_deleted=False).select_related('parent')
    serializer_class = LookupTypeSerializer

    set_ordering_fields = True
    ordering_fields_mapping = {
        'name': 'name',
        'key': 'key'
    }
    ordering_fields = list(ordering_fields_mapping.values())
    ordering = ('-id',)
    search_fields = ['name', 'key']

    filterset_fields = []
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]


class LookupViewSet(ModelViewSet):
    queryset = Lookup.objects.filter(is_deleted=False).select_related('parent').select_related('lookup_type')
    serializer_class = LookupSerializer

    set_ordering_fields = True
    ordering_fields_mapping = {
        'name': 'name',
        'key': 'key'
    }
    ordering_fields = list(ordering_fields_mapping.values())
    ordering = ('-id',)
    search_fields = ['name', 'key']

    filterset_fields = []
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]