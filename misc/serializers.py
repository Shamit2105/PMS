from numpy.char import strip
from rest_framework import serializers
from django.db import transaction
from base.serializers import BaseModelSerializer
from .models import Address,City,State,Country

class CountrySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Country
        fields = ["id",'name','code']


class CountryCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model= Country
        fields = ["id",'name','code',]

    def validate(self,attrs):
        name = attrs['name']
        code = attrs['code']

        name = name.strip()
        code = code.strip()

        if not name.isupper():
            raise serializers.ValidationError("Country name must only contain Capital Alphabets")

        if not code.isupper():
            raise serializers.ValidationError("Country code must only contain Capital Alphabets")

        return attrs

    
class StateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = State
        fields = ["id",'name','code','country']
    
class StateCreateUpdateSerializer():
    class Meta(BaseModelSerializer.Meta):
        model= State
        fields = ['name','code','country']

    def validate(self,attrs):
        name = attrs['name']
        code = attrs['code']

        name = name.strip()
        code = code.strip()

        if not name.isupper():
            raise serializers.ValidationError("State name must only contain Capital Alphabets")

        if not code.isupper():
            raise serializers.ValidationError("State code must only contain Capital Alphabets")

        return attrs

   

class CitySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = City
        fields = ["id",'name','code','state']

class CityCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model= City
        fields = ['name','code','state']

    def validate(self,attrs):
        name = attrs['name']
        code = attrs['code']

        name = name.strip()
        code = code.strip()

        if not name.isupper():
            raise serializers.ValidationError("City name must only contain Capital Alphabets")

        if not code.isupper():
            raise serializers.ValidationError("City code must only contain Capital Alphabets")

        return attrs

class AddressSerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(
        source="city",
        read_only=True
    )
    city_name = serializers.CharField(source="city.name", read_only=True)

    state_id = serializers.PrimaryKeyRelatedField(
        source="city.state",
        read_only=True
    )
    state_name = serializers.CharField(source="city.state.name", read_only=True)

    country_id = serializers.PrimaryKeyRelatedField(
        source="city.state.country",
        read_only=True
    )
    country_name = serializers.CharField(source="city.state.country.name", read_only=True)

    class Meta:
        model = Address
        fields = [
            "id",
            "primary_address",
            "secondary_address",
            "pincode",
            "city_id",
            "city_name",
            "state_id",
            "state_name",
            "country_id",
            "country_name",
        ]


    
class AddressCreateUpdateSerializer(BaseModelSerializer):
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all()
    )
    class Meta(BaseModelSerializer.Meta):
        model = Address
        fields = ['primary_address','secondary_address','pincode','city']

    def validate_pincode(self, value):
        
        if len(value)!=6:
            raise serializers.ValidationError("Pincode must be of 6 digits only!")

        if not value.isdigit():
            raise serializers.ValidationError("Pincode must only contain numbers!")
        
        return value