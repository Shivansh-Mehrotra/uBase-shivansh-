from django.contrib.auth import get_user_model
from django.db import models
from core.db.models import ActivatorModelMixin, ActivatorModelMixinManager

User = get_user_model()


class Question(ActivatorModelMixin, models.Model):
    question = models.CharField(max_length=255)

    objects = ActivatorModelMixinManager()

    def __str__(self):
        return self.question

    class Meta:
        permissions = ()


class Option(models.Model):
    option = models.CharField(max_length=255)
    order = models.IntegerField(default=1)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options', related_query_name='option'
    )

    polling = models.ManyToManyField(
        User, related_name='poll', related_query_name='poll'
    )