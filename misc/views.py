from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from base.views import BaseViewSet
from .models import Country
from .serializers import (CountryCreateUpdateSerializer,CountrySerializer,StateCreateUpdateSerializer,StateSerializer,
                          CityCreateUpdateSerializer,CitySerializer,AddressSerializer,AddressCreateUpdateSerializer)


class CountryViewSet(BaseViewSet,viewsets.ModelViewSet):
    queryset = Country.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name','code']
    ordering_fields = ['name','code','created_at']

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CountryCreateUpdateSerializer
        return CountrySerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            self.perform_create(serializer)
            
            response_serializer = CountrySerializer(serializer.instance)
            return Response(
                {
                    'data': response_serializer.data
                }
                ,status=status.HTTP_201_CREATED
            )
        
        except ValidationError as e:
            return Response(
                {
                    "error":e.detail
                }
                ,status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {

                    'error':str(e)
                }
                ,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class StateViewSet(BaseViewSet,viewsets.ModelViewSet):
    queryset = Country.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name','code','country']
    ordering_fields = ['name','code','created_at','country']

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return StateCreateUpdateSerializer
        return StateSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            self.perform_create(serializer)
            
            response_serializer = StateSerializer(serializer.instance)
            return Response(
                {
                    'data': response_serializer.data
                }
                ,status=status.HTTP_201_CREATED
            )
        
        except ValidationError as e:
            return Response(
                {
                    "error":e.detail
                }
                ,status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {

                    'error':str(e)
                }
                ,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CityViewSet(BaseViewSet,viewsets.ModelViewSet):
    queryset = Country.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name','code','state']
    ordering_fields = ['name','code','created_at','state']

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CityCreateUpdateSerializer
        return CitySerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            self.perform_create(serializer)
            
            response_serializer = CitySerializer(serializer.instance)
            return Response(
                {
                    'data': response_serializer.data
                }
                ,status=status.HTTP_201_CREATED
            )
        
        except ValidationError as e:
            return Response(
                {
                    "error":e.detail
                }
                ,status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {

                    'error':str(e)
                }
                ,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class AddressViewSet(BaseViewSet,viewsets.ModelViewSet):
    queryset = Country.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['pincode','city']
    ordering_fields = ['pincode','created_at','city']

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return AddressCreateUpdateSerializer
        return AddressSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            self.perform_create(serializer)
            
            response_serializer = CitySerializer(serializer.instance)
            return Response(
                {
                    'data': response_serializer.data
                }
                ,status=status.HTTP_201_CREATED
            )
        
        except ValidationError as e:
            return Response(
                {
                    "error":e.detail
                }
                ,status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {

                    'error':str(e)
                }
                ,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )