from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    UserProfileSignupView,
    UserLoginView,
    UserProfileViewSet
)

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('api/auth/signup/', UserProfileSignupView.as_view(), name='user-signup'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    
    path('api/', include(router.urls)),
]