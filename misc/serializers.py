# misc/serializers.py
from rest_framework import serializers
from django.db import transaction
from .models import Address, Country, City, State
from base.serializers import BaseModelSerializer

class CountryListSerializer(BaseModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'is_active', 'created_at', 'updated_at']
        read_only_fields = fields


class StateListSerializer(BaseModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = State
        fields = ['id', 'name', 'code', 'country', 'country_name', 
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = fields


class CityListSerializer(BaseModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    country_name = serializers.CharField(source='state.country.name', read_only=True)
    
    class Meta:
        model = City
        fields = ['id', 'name', 'code', 'state', 'state_name', 'country_name',
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = fields


class AddressListSerializer(BaseModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    state_name = serializers.CharField(source='city.state.name', read_only=True)
    country_name = serializers.CharField(source='city.state.country.name', read_only=True)
    
    class Meta:
        model = Address
        fields = ['id', 'primary_address', 'secondary_address', 'pincode',
                 'city', 'city_name', 'state_name', 'country_name',
                 'created_at', 'updated_at']
        read_only_fields = fields

class CountryCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'code']
    
    def validate_name(self, value):
        value = value.strip()
        if self.instance:  
            qs = Country.objects.filter(name__iexact=value).exclude(id=self.instance.id)
        else: 
            qs = Country.objects.filter(name__iexact=value)
        
        if qs.exists():
            raise serializers.ValidationError(f'Country "{value}" already exists')
        return value
    
    def validate_code(self, value):
        if value:
            value = value.strip().upper()
            if self.instance:
                qs = Country.objects.filter(code=value).exclude(id=self.instance.id)
            else:  
                qs = Country.objects.filter(code=value)
            
            if qs.exists():
                raise serializers.ValidationError(f'Country code "{value}" already exists')
        return value


class StateCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = State
        fields = ['name', 'code', 'country']
    
    def validate(self, attrs):
        name = attrs['name']
        country = attrs['country']
        
        if name and country:
            name = name.strip()
            qs = State.objects.filter(name__iexact=name, country=country)
            
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            
            if qs.exists():
                raise serializers.ValidationError({
                    'name': f'State "{name}" already exists in {country.name}'
                })
        
        if 'code' in attrs:
            attrs['code'] = attrs['code'].strip().upper()
        
        return attrs


class CityCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'code', 'state']
    
    def validate(self, attrs):
        name = attrs['name']
        state = attrs['state']
        
        if name and state:
            name = name.strip()
            qs = City.objects.filter(name__iexact=name, state=state)
            
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            
            if qs.exists():
                raise serializers.ValidationError({
                    'name': f'City "{name}" already exists in {state.name}, {state.country.name}'
                })
        
        if 'code' in attrs:
            attrs['code'] = attrs['code'].strip().upper()
        
        return attrs


class AddressCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Address
        fields = ['primary_address', 'secondary_address', 'pincode', 'city']
    
    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError('Pincode must be 6 digits')
        return value