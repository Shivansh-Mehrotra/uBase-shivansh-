from django.db import models

from core.db.models import ActivatorModelMixin, ActivatorModelMixinManager


class LookupType(ActivatorModelMixin, models.Model):
    name = models.CharField("Lookup Type Name", max_length=50)
    key = models.CharField("Lookup Type key", max_length=50)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    objects = ActivatorModelMixinManager()

    class Meta:
        db_table = 'lookup_type'

    def __str__(self):
        return self.name


class Lookup(ActivatorModelMixin, models.Model):
    lookup_type = models.ForeignKey(LookupType, on_delete=models.CASCADE,
                                    related_query_name='lookup', related_name='lookups')
    parent = models.ForeignKey("self",verbose_name="Parent Lookup", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Lookup name", max_length=50)
    key = models.CharField("Lookup key", max_length=50)
    order = models.IntegerField("Lookup order", null=True, blank=True, default=0)
    info_1 = models.CharField(max_length=255, null=True, blank=True)
    info_2 = models.CharField(max_length=255, null=True, blank=True)
    # TODO: add func for admin managed and app managed
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    objects = ActivatorModelMixinManager()

    class Meta:
        db_table = 'lookup'

    def __str__(self):
        return self.name
