from django.db import models

from core.db.models import ActivatorModelMixin, ActivatorModelMixinManager


class Country(ActivatorModelMixin, models.Model):
    name = models.CharField("Country Name", max_length=50)
    code = models.CharField("Country Code", max_length=50)
    mobile_code = models.CharField("Mobile code country wise", max_length=50, null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    objects = ActivatorModelMixinManager()

    class Meta:
        db_table = 'country'

    def __str__(self):
        return self.name


class State(ActivatorModelMixin, models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states",
                                related_query_name="state")
    name = models.CharField("State Name", max_length=50)
    code = models.CharField("State Code", max_length=50)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    objects = ActivatorModelMixinManager()

    class Meta:
        db_table = 'state'

    def __str__(self):
        return self.name


class City(ActivatorModelMixin, models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities",
                              related_query_name="city")
    name = models.CharField("City Name", max_length=50)
    code = models.CharField("City Code", max_length=50)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    objects = ActivatorModelMixinManager()

    class Meta:
        db_table = 'city'

    def __str__(self):
        return self.name


class Locality(ActivatorModelMixin, models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="localities",
                              related_query_name="locality")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="localities",
                             related_query_name="locality")
    name = models.CharField("Locality Name", max_length=150)
    code = models.CharField("Locality Code", max_length=50)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    objects = ActivatorModelMixinManager()

    class Meta:
        db_table = 'locality'

    def __str__(self):
        return self.name
