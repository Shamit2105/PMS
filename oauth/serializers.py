from django.contrib.auth import get_user_model
from rest_framework import serializers
from allauth.socialaccount.models import SocialAccount
from django.db import transaction

from users.models import UserProfile
from base.serializers import BaseModelSerializer
from misc.serializers import AddressCreateUpdateSerializer
from misc.models import Address

class OAuthUserProfileCreateSerializer(BaseModelSerializer):
    class Meta:
        model = UserProfile

        fields= ['first_name','last_name','dob','contact_number','address',]

    def validate(self, attrs):
        request = self.context['request']
        user_id = request.user
        if UserProfile.objects.filter(user=user_id).exists():
            raise serializers.ValidationError("Profile already exists for this user")
        return attrs
        
class OAuthUserProfileUpdateSerializer(BaseModelSerializer):
    address = AddressCreateUpdateSerializer(required=False)
    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        fields = ['first_name','last_name','contact_number','address',]


    def update(self, instance, validated_data):
        address_data = validated_data.pop("address",None)
        
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            instance.save()

            if address_data:
                address_instance = instance.address
                if address_instance:
                    for attr, value in address_data.items():
                        setattr(address_instance, attr, value)
                    address_instance.save()
                else:
                    new_address = Address.objects.create(**address_data)
                    instance.address = new_address
                    instance.save()
                  
            return instance


class OAuthUserProfileViewSerializer(BaseModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    auth_provider = serializers.SerializerMethodField()
    github_username = serializers.SerializerMethodField()

    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        fields = [
            'username','first_name','last_name','contact_number','address','auth_provider','github_username','email']
        read_only_fields = fields

    def get_auth_provider(self, obj):
        social = SocialAccount.objects.filter(user=obj.user).first()
        return social.provider if social else 'password'

    def get_github_username(self, obj):
        social = SocialAccount.objects.filter(
            user=obj.user,
            provider='github'
        ).first()
        if social:
            return social.extra_data.get('login')
        return None

        
