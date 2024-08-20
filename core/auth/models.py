from _blake2 import blake2b

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.postgres.fields import JSONField
from django.db import models
from core.db.models import ActivatorModelMixin
from core.tokens import make_token

User = get_user_model()


class UserEventToken(ActivatorModelMixin, models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='event_tokens', related_query_name='event_token'
    )
    token = models.TextField()
    valid_for_seconds = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=255)
    meta_value = JSONField(default={}, null=True, blank=True)

    @staticmethod
    def create_token(user, valid_for_seconds=None, type=None, meta_value=None):
        if meta_value is None:
            meta_value = dict()

        token_str = make_token(meta_value)
        token = UserEventToken(
            user=user,
            valid_for_seconds=valid_for_seconds,
            type=type,
            meta_value=meta_value,
            token=token_str
        )
        token.save()
        return token

    #TODO: write check token
    #TODO: write get data by token
    #TODO: invalidate token Exception class

