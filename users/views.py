from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
import logging

from .models import UserProfile
from .serializers import (
    UserProfileSignupSerializer,
    
    UserProfileUpdateSerializer,
    UserProfileViewSerializer,
    CustomTokenObtainPairSerializer
)

User = get_user_model()

logger = logging.getLogger(__name__)

class UserProfileSignupView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSignupSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        
        try:
            logger.info(
                "Signup attempt",
                extra={"user_id": getattr(self.request.user, "id", None)}
            )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
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

        except ValidationError as e:
            logger.error("User Signup failed because of ",+ str(e))
            return Response(

                e.detail or e.default_detail,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.exception("User signup failed because of "+ str(e))
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        try:
            profile = request.user.profiles
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "Profile does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ GET → READ serializer ONLY
        if request.method == "GET":
            serializer = UserProfileViewSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # ✅ PATCH → WRITE serializer ONLY
        write_serializer = UserProfileUpdateSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        write_serializer.is_valid(raise_exception=True)
        write_serializer.save()

        # ✅ return READ serializer again
        read_serializer = UserProfileViewSerializer(profile)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action=='patch':
            return UserProfileUpdateSerializer
        return UserProfileViewSerializer
    
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
        serializer.save(user=self.request.user)
    
    def perform_update(self,serializer):
        serializer.save(updated_by=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info("Trying to create a user profile.")
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.errors)
           
            self.perform_create(serializer)

            response_serializer = UserProfileViewSerializer(serializer.instance)
            logger.info("User Profile Created Successfully")
            return Response(
                data=response_serializer.data,
                status= status.HTTP_201_CREATED
            
            )
        
        except ValidationError as e:
            logger.error("User Profile Creation failed due to error "+ str(e))
            return Response(
                data= e.detail,
                status = status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.exception("User Profile Creation failed due to exception "+ str(e))
            return Response(
                data = str(e),
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def update(self, request, *args, **kwargs):
        logger.info("Trying to update a user profile.")
        instance = self.get_object()
        partial = kwargs.pop('partial',False)
        try:

            serializer = self.get_serializer(instance,data=request.data,partial=partial)
            serializer.is_valid(raise_exception=True)
            if not serializer.is_valid():
                print(serializer.errors)
           
            self.perform_update(serializer)

            response_serializer = UserProfileViewSerializer(serializer.instance)
            logger.info("User Profile Updated Successfully")
            return Response(
                data=response_serializer.data,
                status= status.HTTP_201_CREATED
            
            )
        
        except ValidationError as e:
            logger.error("User Profile updates failed due to error "+str(e))
            return Response(
                data= e.detail,
                status = status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.exception("User Profile Updates failed due to exception "+str(e))
            return Response(
                data = str(e),
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
