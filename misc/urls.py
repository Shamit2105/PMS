from rest_framework.routers import DefaultRouter
from django.urls import path,include

from .views import CountryViewSet,StateViewSet,CityViewSet

router=DefaultRouter()
router.register(r'countries',CountryViewSet,basename='countries')
router.register(r'states',StateViewSet,basename='states')
router.register(r'cities',CityViewSet,basename='cities')


urlpatterns=[
    path("",include(router.urls))
]