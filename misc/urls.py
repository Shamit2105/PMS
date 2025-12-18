from rest_framework.routers import DefaultRouter
from django.urls import path,include

from .views import CountryViewSet

country_router = DefaultRouter()
country_router.register(r"",CountryViewSet,basename='country')


urlpatterns=[
    path("countries/",include(country_router.urls))
]