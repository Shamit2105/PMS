from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect


from .authentication import CsrfExemptSessionAuthentication
from base.views import BaseViewSet
from users.models import UserProfile
from .serializers import OAuthUserProfileCreateSerializer,OAuthUserProfileViewSerializer,OAuthUserProfileUpdateSerializer

class OAuthUserProfileViewSet(BaseViewSet, viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create']:
            return OAuthUserProfileCreateSerializer
        
        elif self.action in ['update','partial_update','patch']:
            return OAuthUserProfileUpdateSerializer
        
        return OAuthUserProfileViewSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.errors)
           
            self.perform_create(serializer)

            response_serializer = OAuthUserProfileViewSerializer(serializer.instance)

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

            response_serializer = OAuthUserProfileViewSerializer(serializer.instance)

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
        
    
        

def github_oauth_callback(request):
    """
    Called AFTER successful GitHub OAuth
    """
    user = request.user

    refresh = RefreshToken.for_user(user)

    access = str(refresh.access_token)
    refresh = str(refresh)

    # Redirect frontend with tokens
    frontend_url = (
        f"http://localhost:8000/oauth/callback"
        f"?access={access}&refresh={refresh}"
    )

    return redirect(frontend_url)