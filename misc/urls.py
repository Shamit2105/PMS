from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CountryViewSet, StateViewSet, 
    CityViewSet, AddressViewSet
)

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'states', StateViewSet, basename='state')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('api/', include(router.urls)),
]