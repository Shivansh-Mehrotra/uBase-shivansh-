from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class ActivatorQuerySet(models.query.QuerySet):
    def exclude_deleted(self):
        return self.filter(is_deleted=False)

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class ActivatorModelMixinManager(models.Manager):
    """
    Manager: SomeModel.objects.active() / .inactive()
    """
    def get_queryset(self):
        qs = ActivatorQuerySet(model=self.model, using=self._db)
        return qs.exclude_deleted()

    def all_objects(self):
        return ActivatorQuerySet(model=self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()


class ActivatorModelMixin(models.Model):
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_deleted = models.BooleanField(
        _('Is Deleted'), default=False,
        help_text="Used for soft delete."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# TODO: new abs class for created by updated by cascade do nothing