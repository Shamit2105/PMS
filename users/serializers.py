from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile
from base.serializers import BaseModelSerializer
from misc.models import Address, City, State, Country

User = get_user_model()

class UserProfileSignupSerializer(BaseModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        fields = [
            'id', 'username', 'password', 'confirm_password', 
            'first_name', 'last_name', 'dob', 'contact_number'
        ]
        
    
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
           
        user = User.objects.create_user(username=username, password=password)
            
        validated_data['user'] = user
        return UserProfile.objects.create(**validated_data)



class UserProfileUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        fields = [
            'id', 'first_name', 'last_name', 'dob', 'contact_number','address'
        ]
        read_only_fields = ['id','dob']
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            instance.save()
            return instance

class UserProfileViewSerializer(BaseModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        fields = [
            'id', 'username', 'first_name', 'last_name', 'dob',
            'contact_number', 'address','address'
        ]
        read_only_fields = fields

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        profile = UserProfile.objects.get(user=self.user)

        data['user'] = {
            'id': profile.id,
            'username': self.user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': self.user.email,
        }

        return data