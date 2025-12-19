from django.urls import include,path
from rest_framework.routers import DefaultRouter

from .views import OAuthUserProfileViewSet,github_oauth_callback

router = DefaultRouter()

router.register(r"",OAuthUserProfileViewSet,basename='user_profiles')


urlpatterns=[
    path('',include(router.urls)),
    path("github/success/", github_oauth_callback),
]