from rest_framework import serializers
from django.db import transaction
from core.apps.permission.models import RoleModuleAction, ModuleAction
from core.apps.role.models import Role, AppSource
from django.db.models import Q
import random
import string

from core.utils.crypto import get_salt_string


class RoleSerializers(serializers.ModelSerializer):
    default_module_action_id = serializers.PrimaryKeyRelatedField(
        error_messages={
            'does_not_exist': "Module Action with id '{pk_value}' does not exist."
        },
        source='default_module_action', queryset=ModuleAction.objects.all(), allow_null=True, default=None, 
        required=False
    )
    default_module_action = serializers.CharField(source='default_module_action.action', read_only=True, default=None)
    default_module_action_label = serializers.CharField(source='default_module_action.label', read_only=True, default=None)

    app_source_id = serializers.PrimaryKeyRelatedField(
        source='app_source', queryset=AppSource.objects.all(), required=True
    )
    app_source_label = serializers.CharField(source='app_source.label', read_only=True, default=None)

    module_actions = serializers.PrimaryKeyRelatedField(
        queryset=ModuleAction.objects.all(), many=True, allow_empty=True,
        error_messages={
            'does_not_exist': "Module Action with id '{pk_value}' does not exist."
        }
    )

    class Meta:
        model = Role
        fields = (
            'id', 'name', 'key', 'description', 'default_module_action_id', 'default_module_action_label',
            'default_module_action', 'app_source_id', 'app_source_label', 'is_active', 'created_by',
            'updated_by', 'module_actions'
        )

    def validate_name(self, value):
        qs = Role.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.filter(~Q(id=self.instance.id))
        if qs.exists():
            raise serializers.ValidationError('Role already exists.')
        return value

    def validate_key(self, value):
        qs = Role.objects.filter(key__iexact=value)
        if self.instance:
            qs = qs.filter(~Q(id=self.instance.id))
        if qs.exists():
            raise serializers.ValidationError('Role key is already exists.')
        return value

    def _get_module_actions_from_validated_data(self, validated_data):
        if 'module_actions' in validated_data:
            return validated_data.pop('module_actions')

    # def create(self, validated_data):
    #     module_actions = self._get_module_actions_from_validated_data(validated_data)
    #     with transaction.atomic():
    #         role = Role.objects.create(**validated_data)
    #         if module_actions:
    #             role.module_actions.add(*[ma.id for ma in module_actions])
    #     return role

    # def update(self, instance, validated_data):
    #     # TODO: add array for module action ids
    #     with transaction.atomic():
    #         super().update(instance, validated_data)
    #         # TODO: add array for module action ids
    #     return instance

    # TODO: add array for module action ids


class AppSourceSerializers(serializers.ModelSerializer):
    salt_key = serializers.CharField(required=False)

    class Meta:
        model = AppSource
        fields = (
            'id',
            'label',
            'source_key',
            'salt_key',
            'description',
            'is_active',
        )

    def _get_unique_salt_key(self):
        salt_key = get_salt_string(50)
        if not AppSource.objects.filter(salt_key=salt_key).exists():
            return salt_key
        else:
            '''
            This recursion this useful if the created `salt_key` already exists  
            '''
            return self._get_unique_salt_key()

    def validate_source_key(self, value):
        qs = AppSource.objects.filter(source_key__iexact=value)
        if self.instance:
            qs = qs.filter(~Q(id=self.instance.id))
        if qs.exists():
            raise serializers.ValidationError('App Source key is already exists.')
        return value

    def create(self, validated_data):
        if 'salt_key' not in validated_data:
            validated_data['salt_key'] = self._get_unique_salt_key()
        app_source = AppSource.objects.create(**validated_data)
        return app_source