from django.db import models
from django.utils.translation import gettext_lazy as _
from core.apps.role.models import Role


class PermissionsMixin(models.Model):
    roles = models.ManyToManyField(
        Role,
        verbose_name=_('roles'),
        blank=True,
        help_text=_(
            'The roles this user belongs to. A user will get all permissions '
            'granted to each of their roles.'
        ),
        related_name="users",
        related_query_name="user",
    )

    module_actions = models.ManyToManyField(
        'permission.ModuleAction',
        verbose_name='module_actions',
        blank=True,
        help_text="To map role with BE permission in case needed",
        through='permission.UserModuleAction',
        related_name='users', related_query_name='user'
    )

    class Meta:
        abstract = True
