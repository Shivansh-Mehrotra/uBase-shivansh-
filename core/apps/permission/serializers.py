from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers
from core.apps.permission.models import Module, ModuleAction, UserModuleAction
from django.db.models import Q
from django.db import transaction
from core.apps.role.models import AppSource

User = get_user_model()


class ModuleSerializers(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent', queryset=Module.objects.all(), allow_null=True, default=None, required=False
    )
    app_source_id = serializers.PrimaryKeyRelatedField(
        source='app_source', queryset=AppSource.objects.all(), allow_null=True, default=None, required=False
    )
    parent_module_label = serializers.CharField(
        source='parent.label', default=None, read_only=True, allow_blank=False
    )
    parent_module_key = serializers.CharField(
        source='parent.module_key', default=None, read_only=True, allow_blank=False
    )
    module_action_data = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = (
            'id',
            'module_key',
            'label',
            'description',
            'app_source_id',
            'order',
            'parent_id',
            'parent_module_label',
            'parent_module_key',
            'module_action_data',
        )

    def validate_module_key(self, value):
        mqs = Module.objects.filter(module_key__iexact=value)

        if self.instance:
            mqs = mqs.filter(~Q(module_key=self.instance.module_key))

        if mqs.exists():
            raise serializers.ValidationError('Module key already exists.')

        return value

    def get_module_action_data(self, obj):
        module_action_list = []
        module_action_data = ModuleAction.objects.active().filter(module=obj)
        for module_action in module_action_data:
            module_action_list.append(
                {
                    'description': module_action.description,
                    'action': module_action.action,
                    'label': module_action.label,
                    'route_url': module_action.route_url,
                    'is_routable': module_action.is_routable,
                    'module_id': module_action.module_id,
                    'created_at': module_action.created_at,
                    'updated_at': module_action.updated_at,
                }
            )
        return module_action_list


class ModuleActionPermissionSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), required=True,
        error_messages={
            'does_not_exist': "Permission with id '{pk_value}' does not exist."
        }
    )

    class Meta:
        model = Permission
        fields = [
            'id', 'codename', 'name'
        ]
        extra_kwargs = {
            'name': {'read_only': True},
            'codename': {'read_only': True},
        }


class ModuleActionSerializers(serializers.ModelSerializer):
    module_label = serializers.CharField(source='module.label', read_only=True, default=None)
    module_key = serializers.CharField(source='module.module_key', read_only=True, default=None)
    module_id = serializers.PrimaryKeyRelatedField(
        source='module', queryset=Module.objects.all()
    )
    permissions = ModuleActionPermissionSerializers(many=True, required=False, allow_null=True)

    class Meta:
        model = ModuleAction
        fields = (
            'id',
            'action',
            'label',
            'description',
            'route_url',
            'is_routable',
            'module_id',
            'module_label',
            'module_key',
            'order',
            'is_active',
            'permissions',
        )

    def validate(self, data, *args, **kwargs):
        if 'action' in data:
            qs = ModuleAction.objects.filter(
                action__iexact=data['action'], module_id=data['module_id']
            )
            if self.instance:
                qs = qs.filter(~Q(id=self.instance.id))
            if qs.exists():
                raise serializers.ValidationError({'action': 'Module action is already exists.'})

        return data

    def _get_permission_from_validated_data(self, validated_data):
        if 'permissions' in validated_data:
            return validated_data.pop('permissions')

    def update(self, instance, validated_data):
        permissions = self._get_permission_from_validated_data(validated_data)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            if permissions is not None:
                # instance.permissions.clear()
                instance.permissions.set([p['id'] for p in permissions])
            return instance

    def create(self, validated_data):
        permissions = self._get_permission_from_validated_data(validated_data)
        with transaction.atomic():
            action = ModuleAction.objects.create(**validated_data)
            if permissions:
                action.permissions.add(*[p['id'].id for p in permissions])
            return action


# class RoleModuleActionSerializers(serializers.ModelSerializer):
#     role_id = serializers.IntegerField(required=True, write_only=True)
#     module_action_id = serializers.ListField(required=True, write_only=True,
#                                              child=serializers.IntegerField(min_value=1))
#
#     class Meta:
#         model = RoleModuleAction
#         fields = [
#             'id',
#             'role_id',
#             'module_action_id',
#             'created_by'
#         ]
#         extra_kwargs = {
#             'created_by': {'write_only': True}
#         }
#
#     def create(self, validated_data):
#         RoleModuleAction.objects.filter(role_id=validated_data['role_id']).update(is_deleted=True)
#         role_module_action_list = []
#         for module_action_id in validated_data['module_action_id']:
#             role_module_action_list.append(RoleModuleAction(**{
#                 'role_id': validated_data['role_id'],
#                 'module_action_id': module_action_id,
#                 'created_by': validated_data['created_by']
#             }))
#         RoleModuleAction.objects.bulk_create(role_module_action_list)
#         return True
#
#
class UserModuleActionSerializers(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all()
    )
    module_actions = serializers.PrimaryKeyRelatedField(
        queryset=ModuleAction.objects.all(), many=True, allow_empty=True, write_only=True,
        error_messages={
            'does_not_exist': "Module Action with id '{pk_value}' does not exist."
        }
    )
    created_by = serializers.IntegerField(allow_null=True, required=False, write_only=True)

    def create(self, validated_data):
        UserModuleAction.objects.filter(user_id=validated_data['user_id']).update(is_deleted=True)
        user_module_action_list = []
        for module_action in validated_data['module_actions']:
            user_module_action_list.append(UserModuleAction(**{
                'user': validated_data['user_id'],
                'module_action': module_action,
                'created_by': validated_data['created_by']
            }))
        UserModuleAction.objects.bulk_create(user_module_action_list)
        return True
