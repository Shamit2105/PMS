from base.models import BaseModel
from django.db import models


class Country(BaseModel):
    name=models.CharField(max_length=50)
    code = models.CharField(max_length=10)

class State(BaseModel):
    name=models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    country_id = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='states')

class City(BaseModel):
    name=models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    state_id=models.ForeignKey(to=State, on_delete=models.CASCADE, related_name='cities')

class Address(BaseModel):
    primary_address = models.TextField()
    secondary_address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=6)
    city_id = models.ForeignKey(to=City, on_delete=models.CASCADE)

