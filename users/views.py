from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import (
    UserProfileSignupSerializer,
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    UserProfileViewSerializer,
    AddAddressToProfileSerializer,
    CreateAddressForProfileSerializer
)

User = get_user_model()

class UserProfileSignupView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSignupSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation failed',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            instance = serializer.save()
            
            refresh = RefreshToken.for_user(instance.user)
            
            response_data = {
                'success': True,
                'message': 'User registered successfully',
                'data': {
                    'user': {
                        'id': instance.id,
                        'username': instance.user.username,
                        'first_name': instance.first_name,
                        'last_name': instance.last_name,
                        'email': instance.user.email,
                    },
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                }
            }
            
            headers = self.get_success_headers(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
            
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Error creating user',
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Login failed',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        user_profile = data['user_profile']
        
        return Response(
            {
                'success': True,
                'message': 'Login successful',
                'data': {
                    'user': {
                        'id': user_profile.id,
                        'username': data['user'].username,
                        'first_name': user_profile.first_name,
                        'last_name': user_profile.last_name,
                        'email': data['user'].email,
                    },
                    'tokens': {
                        'access': data['access'],
                        'refresh': data['refresh'],
                    }
                }
            },
            status=status.HTTP_200_OK
        )

class UserProfileViewSet(viewsets.GenericViewSet,generics.RetrieveAPIView,generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return UserProfileUpdateSerializer
        return UserProfileViewSerializer
    
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='address/create')
    def create_new_address(self, request):
        user_profile = self.get_object()
        serializer = CreateAddressForProfileSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation failed',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            address = serializer.save()
            user_profile.address = address
            user_profile.save()
            
            profile_serializer = UserProfileViewSerializer(user_profile)
            
            return Response(
                {
                    'success': True,
                    'message': 'Address created and linked to profile successfully',
                    'data': profile_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Error creating address',
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['delete'], url_path='address/remove')
    def remove_address(self, request):
        user_profile = self.get_object()
        
        if not user_profile.address:
            return Response(
                {
                    'success': False,
                    'message': 'No address linked to profile'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_profile.address = None
            user_profile.save()
            
            profile_serializer = UserProfileViewSerializer(user_profile)
            
            return Response(
                {
                    'success': True,
                    'message': 'Address removed from profile successfully',
                    'data': profile_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Error removing address',
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'], url_path='address')
    def get_address(self, request):
        user_profile = self.get_object()
        
        if not user_profile.address:
            return Response(
                {
                    'success': True,
                    'message': 'No address found',
                    'data': None
                },
                status=status.HTTP_200_OK
            )
        
        from misc.serializers import AddressListSerializer
        address_serializer = AddressListSerializer(user_profile.address)
        
        return Response(
            {
                'success': True,
                'message': 'Address retrieved successfully',
                'data': address_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response(
            {
                'success': True,
                'message': 'Profile retrieved successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    