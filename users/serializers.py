from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from base.serializers import BaseModelSerializer
from misc.models import Address, City, State, Country

User = get_user_model()

class UserProfileSignupSerializer(BaseModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'password', 'confirm_password', 
            'first_name', 'last_name', 'dob', 'contact_number'
        ]
        read_only_fields = ['id']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data
    
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists. Please try another one")
        return username
    
    def create(self, validated_data):
        validated_data = dict(validated_data)
        
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        
        with transaction.atomic():
           
            user = User.objects.create_user(username=username, password=password)
            
            validated_data['user'] = user
            
            allowed_fields = {'user', 'first_name', 'last_name', 'dob', 'contact_number'}
            cleaned_data = {k: v for k, v in validated_data.items() if k in allowed_fields}
            
            return UserProfile.objects.create(**cleaned_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("User profile not found")
        
        refresh = RefreshToken.for_user(user)
        
        data['user'] = user
        data['user_profile'] = user_profile
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        return data

class UserProfileUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'first_name', 'last_name', 'dob', 'contact_number'
        ]
        read_only_fields = ['id']
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            instance.save()
            return instance

class UserProfileViewSerializer(BaseModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'dob',
            'contact_number', 'address', 'created_at', 'updated_at',
            'created_by', 'updated_by', 'is_active'
        ]
        read_only_fields = fields


class AddAddressToProfileSerializer(serializers.Serializer):
    address_id = serializers.UUIDField(required=True)
    
    def validate_address_id(self, value):
        
        
        try:
            address = Address.objects.get(id=value, is_active=True)
        except Address.DoesNotExist:
            raise serializers.ValidationError("Address not found or inactive")
        
        return value
    
    def save(self, user_profile):
        
        
        address_id = self.validated_data['address_id']
        address = Address.objects.get(id=address_id)
        
        user_profile.address = address
        user_profile.save()
        return user_profile

class CreateAddressForProfileSerializer(serializers.Serializer):
    city = serializers.UUIDField(write_only=True, required=False)
    city_data = serializers.DictField(write_only=True, required=False)
    
    primary_address = serializers.CharField(required=True)
    secondary_address = serializers.CharField(required=False, allow_blank=True)
    pincode = serializers.CharField(required=True, max_length=6)
    
    def validate(self, attrs):
        city_id = attrs.get('city')
        city_data = attrs.get('city_data')
        
        if not city_id and not city_data:
            raise serializers.ValidationError({
                'city': 'Either city_id or city_data must be provided'
            })
        
        if city_id and city_data:
            raise serializers.ValidationError({
                'city': 'Provide either city_id or city_data, not both'
            })
        
        pincode = attrs.get('pincode', '')
        if not pincode.isdigit() or len(pincode) != 6:
            raise serializers.ValidationError({
                'pincode': 'Pincode must be 6 digits'
            })
        
        return attrs
    
    def create(self, validated_data):
        
        
        city_id = validated_data.pop('city', None)
        city_data = validated_data.pop('city_data', None)
        
        with transaction.atomic():
            city = None
            
            if city_id:
                city = City.objects.get(id=city_id, is_active=True)
            
            elif city_data:
                city_name = city_data.get('name', '').strip()
                city_code = city_data.get('code', '').strip().upper()
                
                state_data = city_data.get('state_data')
                state = None
                
                if state_data:
                    state_name = state_data.get('name', '').strip()
                    state_code = state_data.get('code', '').strip().upper()
                    country_data = state_data.get('country_data')
                    country = None
                    
                    if country_data:
                        country_name = country_data.get('name', '').strip()
                        country_code = country_data.get('code', '').strip().upper()
                        
                        country, _ = Country.objects.get_or_create(
                            name__iexact=country_name,
                            defaults={
                                'name': country_name,
                                'code': country_code
                            }
                        )
                    
                    if country:
                        state, _ = State.objects.get_or_create(
                            name__iexact=state_name,
                            country=country,
                            defaults={
                                'name': state_name,
                                'code': state_code,
                                'country': country
                            }
                        )
                
                if state:
                    city, _ = City.objects.get_or_create(
                        name__iexact=city_name,
                        state=state,
                        defaults={
                            'name': city_name,
                            'code': city_code,
                            'state': state
                        }
                    )
            
            if not city:
                raise serializers.ValidationError({
                    'city': 'Could not find or create city'
                })
            
            address = Address.objects.create(
                city=city,
                primary_address=validated_data.get('primary_address'),
                secondary_address=validated_data.get('secondary_address', ''),
                pincode=validated_data.get('pincode')
            )
            
            return address