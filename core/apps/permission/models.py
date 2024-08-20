from django.contrib.auth.models import Permission
from django.db import models
from core.apps.role.models import AppSource, Role
from core.db.models import ActivatorModelMixin, ActivatorModelMixinManager
from django.utils.translation import gettext_lazy as _


class Module(ActivatorModelMixin, models.Model):
    module_key = models.CharField('Module Key', max_length=50)
    label = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    app_source = models.ForeignKey(
        AppSource, on_delete=models.CASCADE, null=True, blank=True, verbose_name='App Source'
    )
    order = models.IntegerField(null=True, blank=True, default=0)
    objects = ActivatorModelMixinManager()

    class Meta:
        db_table = 'module'

    def __str__(self):
        return self.label


class ModuleAction(ActivatorModelMixin, models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE,
                               related_query_name='module_action', related_name='module_actions')
    action = models.CharField(max_length=50)
    label = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    order = models.IntegerField(null=True, blank=True, default=0)
    route_url = models.CharField(verbose_name='Route Url', max_length=255,null=True,blank=True)
    is_routable = models.BooleanField('Is Routable', default=False)

    objects = ActivatorModelMixinManager()

    permissions = models.ManyToManyField(
        Permission, blank=True
    )

    class Meta:
        db_table = 'module_action'
        verbose_name = 'Module Action'
        verbose_name_plural = 'Module Actions'

    def __str__(self):
        return f'{self.module.label} | {self.label}'


class RoleModuleAction(ActivatorModelMixin, models.Model):
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE
    )
    module_action = models.ForeignKey(
        ModuleAction, on_delete=models.CASCADE, related_name='role_module_actions',
        related_query_name='role_module_action'
    )
    created_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'role_module_action'


class UserModuleAction(ActivatorModelMixin, models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    module_action = models.ForeignKey(ModuleAction, on_delete=models.CASCADE)
    created_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_module_action'

