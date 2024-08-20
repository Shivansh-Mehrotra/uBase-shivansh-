from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers

from core.apps.lookup_management.models import LookupType, Lookup

User = get_user_model()


class LookupTypeSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent', queryset=LookupType.objects.all(), allow_null=True, required=False,
        error_messages={
            'does_not_exist': "Lookup type with id '{pk_value}' does not exist."
        }
    )
    parent_name = serializers.CharField(
        source='parent.name', default=None, read_only=True, allow_blank=False
    )
    parent_key = serializers.CharField(
        source='parent.key', default=None, read_only=True, allow_blank=False
    )

    class Meta:
        model = LookupType
        fields = (
            'id',
            'name',
            'key',
            'parent_id',
            'parent_name',
            'parent_key',
            'is_active',
            'created_at'
        )

    def validate_key(self, value):
        ltqs = LookupType.objects.filter(key__iexact=value)
        if self.instance:
            ltqs = ltqs.filter(~Q(key=self.instance.key))
        if ltqs.exists():
            raise serializers.ValidationError('Lookup type key already exists.')
        return value.upper()


class LookupSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent', queryset=Lookup.objects.all(), allow_null=True, required=False,
        error_messages={
            'does_not_exist': "Lookup with id '{pk_value}' does not exist."
        }
    )
    parent_name = serializers.CharField(
        source='parent.name', default=None, read_only=True
    )
    parent_key = serializers.CharField(
        source='parent.key', default=None, read_only=True
    )

    lookup_type_id = serializers.PrimaryKeyRelatedField(
        source='lookup_type', queryset=LookupType.objects.all(), required=True,
        error_messages={
            'does_not_exist': "Lookup type with id '{pk_value}' does not exist."
        }
    )
    lookup_type_name = serializers.CharField(
        source='lookup_type.name', default=None, read_only=True
    )
    lookup_type_key = serializers.CharField(
        source='lookup_type.key', default=None, read_only=True
    )

    class Meta:
        model = Lookup
        fields = (
            'id',
            'name',
            'key',
            'parent_id',
            'parent_name',
            'parent_key',
            'lookup_type_id',
            'lookup_type_name',
            'lookup_type_key',
            'order',
            'info_1',
            'info_2',
            'is_active',
            'created_at'
        )

    def validate_key(self, value):
        ltqs = Lookup.objects.filter(key__iexact=value)
        if self.instance:
            ltqs = ltqs.filter(~Q(key=self.instance.key))
        if ltqs.exists():
            raise serializers.ValidationError('Lookup type key already exists.')
        return value.upper()





