from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers

from core.apps.locality.models import Country, State, City, Locality

User = get_user_model()


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = (
            'id',
            'name',
            'code',
            'mobile_code',
            'is_active',
            'created_at',
            'created_by',
        )

    def validate_name(self, value):
        cqs = Country.objects.filter(name__iexact=value)
        if self.instance:
            cqs = cqs.filter(~Q(id=self.instance.id))
        if cqs.exists():
            raise serializers.ValidationError('Country name already exists.')
        return value

    def validate_code(self, value):
        cqs = Country.objects.filter(code__iexact=value)
        if self.instance:
            cqs = cqs.filter(~Q(id=self.instance.id))
        if cqs.exists():
            raise serializers.ValidationError('Country code already exists.')
        return value.upper()


class StateSerializer(serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(
        source='country', queryset=Country.objects.all(), required=True,
        error_messages={
            'does_not_exist': "Country with id '{pk_value}' does not exist."
        }
    )
    country_name = serializers.CharField(
        source='country.name', default=None, read_only=True
    )

    class Meta:
        model = State
        fields = (
            'id',
            'name',
            'code',
            'country_id',
            'country_name',
            'is_active',
            'created_at',
            'created_by',
        )

    def validate_name(self, value):
        sqs = State.objects.filter(name__iexact=value)
        if self.instance:
            sqs = sqs.filter(~Q(id=self.instance.id))
        if sqs.exists():
            raise serializers.ValidationError('State name already exists.')
        return value

    def validate_code(self, value):
        sqs = State.objects.filter(code__iexact=value)
        if self.instance:
            sqs = sqs.filter(~Q(id=self.instance.id))
        if sqs.exists():
            raise serializers.ValidationError('State code already exists.')
        return value.upper()


class CitySerializer(serializers.ModelSerializer):
    state_id = serializers.PrimaryKeyRelatedField(
        source='state', queryset=State.objects.all(), required=True,
        error_messages={
            'does_not_exist': "State with id '{pk_value}' does not exist."
        }
    )
    state_name = serializers.CharField(
        source='state.name', default=None, read_only=True
    )

    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'code',
            'state_id',
            'state_name',
            'is_active',
            'created_at',
            'created_by',
        )

    def validate(self, attrs):
        cqs = attrs['state'].cities.filter(Q(name__iexact=attrs['name']) |
                                           Q(code__iexact=attrs['code']))
        if self.instance:
            cqs = cqs.filter(~Q(id=self.instance.id))
        if cqs.exists():
            raise serializers.ValidationError({'city':'City name or code already exists in this State'})
        attrs['code'] = attrs['code'].upper()
        return attrs


class LocalitySerializer(serializers.ModelSerializer):
    state_id = serializers.PrimaryKeyRelatedField(
        source='state', queryset=State.objects.all(), required=True,
        error_messages={
            'does_not_exist': "State with id '{pk_value}' does not exist."
        }
    )
    state_name = serializers.CharField(
        source='state.name', default=None, read_only=True
    )

    city_id = serializers.PrimaryKeyRelatedField(
        source='city', queryset=City.objects.all(), required=True,
        error_messages={
            'does_not_exist': "City with id '{pk_value}' does not exist."
        }
    )

    city_name = serializers.CharField(
        source='city.name', default=None, read_only=True
    )

    class Meta:
        model = Locality
        fields = (
            'id',
            'name',
            'code',
            'landmark',
            'pincode',
            'latitude',
            'city_id',
            'city_name',
            'state_id',
            'state_name',
            'is_active',
            'created_at',
            'created_by',
        )

    def validate(self, attrs):
        lqs = attrs['city'].localities.filter(Q(name__iexact=attrs['name']) |
                                           Q(code__iexact=attrs['code']))
        if self.instance:
            lqs = lqs.filter(~Q(id=self.instance.id))
        if lqs.exists():
            raise serializers.ValidationError({'city':'Locality name or code already exists in this City'})
        attrs['code'] = attrs['code'].upper()
        return attrs






