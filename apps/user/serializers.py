from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.db import transaction

from core.apps.role.models import Role

User = get_user_model()


class UserBaseSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    username = serializers.CharField(required=False)
    roles = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), many=True, required=True, allow_empty=False,
        error_messages={
            'does_not_exist': "Role with id '{pk_value}' does not exist."
        }
    )

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active',
            'is_deleted',
            'created_at',
            'updated_at',
            'roles'
        )


class UserCreateSerializer(UserBaseSerializer):
    password = serializers.CharField(max_length=45, min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(max_length=45, min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = UserBaseSerializer.Meta.fields + ('password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password does not match with confirm password.'})
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['username'] = validated_data['email']
        del validated_data['confirm_password']
        instance = super().create(validated_data)
        return instance


class UserUpdateSerializer(UserBaseSerializer):

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    username = serializers.CharField(required=False)
    role_name = serializers.SerializerMethodField(required=False)
    role_id = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active',
            'created_at',
            'role_name',
            'role_id',
        )

    def get_role_name(self, obj):
        # FIXME: Get role and cache it locally so that 1 sql query can be saved.
        #  also find a way to manage app source and role properly.
        app_source = self.context['request'].headers.get('app-source')
        params = {}
        if app_source:
            params['app_source__source_key'] = app_source
        role_names = obj.roles.filter(**params).values_list('name', flat=True)
        return role_names[0] if role_names else None

    def get_role_id(self, obj):
        # FIXME: Get role and cache it locally so that 1 sql query can be saved.
        #  also find a way to manage app source and role properly.
        app_source = self.context['request'].headers.get('app-source')
        params = {}
        if app_source:
            params['app_source__source_key'] = app_source
        role_names = obj.roles.filter(**params).values_list('id', flat=True)
        return role_names[0] if role_names else None

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')
        instance = super().update(instance, validated_data)
        return instance
