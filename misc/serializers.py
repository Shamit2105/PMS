from numpy.char import strip
from rest_framework import serializers
from django.db import transaction


from base.serializers import BaseModelSerializer
from .models import Address,City,State,Country

class CountrySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Country
        fields = ['name','code']


class CountryCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model= Country
        fields = ['name','code',]

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
        model = Country
        fields = ['name','code','country']
    
class StateCreateUpdateSerializer():
    class Meta(BaseModelSerializer.Meta):
        model= Country
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
        model = Country
        fields = ['name','code','state']

class CityCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model= Country
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

class AddressSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Address
        fields = ['primary_address','secondary_address','pincode','city']

    
class AddressCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Address
        fields = ['primary_address','secondary_address','pincode','city']

    def validate_pincode(self,attrs):
        pincode = attrs['pincode']
        if len(pincode)!=6:
            raise serializers.ValidationError("Pincode must be of 6 digits only!")

        if not pincode.isdigit():
            raise serializers.ValidationError("Pincode must only contain numbers!")
    
