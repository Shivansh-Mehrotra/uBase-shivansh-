from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models
from core.db.models import ActivatorModelMixin, ActivatorModelMixinManager
from django.contrib.auth import get_user_model


class AppSource(ActivatorModelMixin,models.Model):
    label = models.CharField(max_length=255)
    source_key = models.CharField(max_length=55)
    salt_key = models.CharField(max_length=255)
    # api version
    # permission version
    description = models.TextField()

    objects = ActivatorModelMixinManager()

    def __str__(self):
        return f'{self.label}-{self.source_key}'

    class Meta:
        verbose_name = 'App Source'
        verbose_name_plural = 'App Source'


class Role(ActivatorModelMixin, models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    default_module_action = models.ForeignKey(
        'permission.ModuleAction', on_delete=models.CASCADE, null=True, blank=True,
        help_text='This module action will be used as landing page when this role log-in',
        verbose_name='Default Module Action',
        related_name='default_roles', related_query_name='default_roles'
    )
    app_source = models.ForeignKey(
        AppSource, on_delete=models.CASCADE, verbose_name='App Source'
    )
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    is_system_role = models.BooleanField(
        'Is System Role', default=False,
        help_text="Use is flag to distinguish between system role and user defined role"
    )
    # TODO: make management commands for permissions
    
    permissions = models.ManyToManyField(
        Permission,
        verbose_name='permissions',
        blank=True,
        help_text="To map role with BE permission in case needed"
    )

    module_actions = models.ManyToManyField(
        'permission.ModuleAction',
        verbose_name='module_actions',
        blank=True,
        help_text="To map role with BE permission in case needed",
        through='permission.RoleModuleAction',
        related_name='roles', related_query_name='role'
    )

    objects = ActivatorModelMixinManager()

    class Meta:
        db_table = 'role'

    def __str__(self):
        return self.name

