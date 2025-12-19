from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.serializers import ValidationError

from .models import UserProfile
from .serializers import (
    UserProfileSignupSerializer,
    
    UserProfileUpdateSerializer,
    UserProfileViewSerializer,
    CustomTokenObtainPairSerializer
)

User = get_user_model()

class UserProfileSignupView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSignupSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)

            instance = serializer.save()
            
            refresh = RefreshToken.for_user(instance.user)
            
            response_data = {
                
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
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileViewSet(viewsets.GenericViewSet,generics.RetrieveAPIView,generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action=='patch':
            return UserProfileUpdateSerializer
        return UserProfileViewSerializer
    
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)
    
    
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
    def perform_create(self, serializer):
        # 🔑 IMPORTANT: bind OAuth user explicitly
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # 🔑 IMPORTANT: DO NOT pass updated_by here
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.errors)
           
            self.perform_create(serializer)

            response_serializer = UserProfileViewSerializer(serializer.instance)

            return Response(
                data=response_serializer.data,
                status= status.HTTP_201_CREATED
            
            )
        
        except ValidationError as e:
            return Response(
                data= e.detail,
                status = status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                data = str(e),
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial',False)

        try:

            serializer = self.get_serializer(instance,data=request.data,partial=partial)
            serializer.is_valid(raise_exception=True)
            if not serializer.is_valid():
                print(serializer.errors)
           
            self.perform_update(serializer)

            response_serializer = UserProfileViewSerializer(serializer.instance)

            return Response(
                data=response_serializer.data,
                status= status.HTTP_201_CREATED
            
            )
        
        except ValidationError as e:
            return Response(
                data= e.detail,
                status = status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                data = str(e),
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
