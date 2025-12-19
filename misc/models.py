from base.models import BaseModel
from django.db import models


class Country(BaseModel):
    name=models.CharField(max_length=50,unique=True)
    code = models.CharField(max_length=10)

    class Meta(BaseModel.Meta):
        db_table = 'Countries'

        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class State(BaseModel):
    name=models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='states')

    class Meta:
        db_table = 'States'

        verbose_name = 'State'
        verbose_name_plural = 'States'
        constraints = [
            models.UniqueConstraint(fields=['name', 'country'], name='unique_state_name_per_country'),
            models.UniqueConstraint(fields=['code', 'country'], name='unique_state_code_per_country')
        ]

class City(BaseModel):
    name=models.CharField(max_length=50,)
    code = models.CharField(max_length=10,)
    state=models.ForeignKey(to=State, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        db_table = 'Cities'

        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        constraints = [
            models.UniqueConstraint(fields=['name', 'state'], name='unique_city_name_per_state'),
            models.UniqueConstraint(fields=['code', 'state'], name='unique_city_code_per_state')
        ]

class Address(BaseModel):
    primary_address = models.TextField()
    secondary_address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=6)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Addresses'

        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
