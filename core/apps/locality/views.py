from django.db.models import Q

from rest_framework.permissions import IsAuthenticated

from core.apps.locality.models import Country, State, City, Locality
from core.apps.locality.serializers import CountrySerializer, StateSerializer, CitySerializer, LocalitySerializer
from core.viewsets import ModelViewSet
from core.permissions import StrictDjangoModelPermissions


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.filter(is_deleted=False)
    serializer_class = CountrySerializer

    ordering_fields_mapping = {}
    ordering_fields = ['name', 'code', 'mobile_code']
    ordering = ('-id',)
    search_fields = ['name', 'code', 'mobile_code']

    filterset_fields_mappings = {}
    filterset_fields = []
    permission_classes = [IsAuthenticated]


class StateViewSet(ModelViewSet):
    queryset = State.objects.filter(is_deleted=False).select_related('country')
    serializer_class = StateSerializer

    ordering_fields_mapping = {
        'country_name': 'country__name'
    }
    ordering_fields = ['name', 'code', 'country_id']
    ordering = ('-id',)
    search_fields = ['name', 'code', 'country__name']

    filterset_fields_mappings = {
        'country_name': 'country__name'
    }
    filterset_fields = ['country_id']
    permission_classes = [IsAuthenticated]


class CityViewSet(ModelViewSet):
    queryset = City.objects.filter(is_deleted=False).select_related('state')
    serializer_class = CitySerializer

    ordering_fields_mapping = {
        'state_name': 'state__name'
    }
    ordering_fields = ['name', 'code', 'state_id']
    ordering = ('-id',)
    search_fields = ['name', 'code', 'state__name']

    filterset_fields_mappings = {
        'state_name': 'state__name'
    }
    filterset_fields = ['state_id']
    permission_classes = [IsAuthenticated]


class LocalityViewSet(ModelViewSet):
    queryset = Locality.objects.filter(is_deleted=False).select_related('state').select_related('city')
    serializer_class = LocalitySerializer

    ordering_fields_mapping = {
        'state_name': 'state__name',
        'city_name': 'city__name'
    }
    ordering_fields = ['name', 'code']
    ordering = ('-id',)
    search_fields = ['name', 'code', 'city__name']

    filterset_fields_mappings = {
        'state_name': 'state__name',
        'city_name': 'city__name'
    }
    filterset_fields = ['state_id', 'city_id']
    permission_classes = [IsAuthenticated]