from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser as DjAbstractUser, UserManager as DjUserManager
from core.auth.mixins import PermissionsMixin
from core.db.models import ActivatorModelMixinManager


class AbstractUser(DjAbstractUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField('Email', max_length=40, unique=True,)
    is_email_verified = models.BooleanField("Email Verification", default=False)
    # TODO: handle phone_number with country code
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta(DjAbstractUser.Meta):
        abstract = True

    def __str__(self):
        return self.email


class UserManager(ActivatorModelMixinManager, DjUserManager):
    pass


# class User(AbstractUser):
#     """
#     Copy this model to your user app to make custom user model
#     """
#     objects = UserManager()
#
#     class Meta(AbstractUser.Meta):
#         db_table = 'auth_user'
#         swappable = 'AUTH_USER_MODEL'
