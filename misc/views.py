
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404

from base.views import BaseViewSet
from .models import Country, State, City, Address
from .serializers import (
    
    CountryListSerializer, StateListSerializer,
    CityListSerializer, AddressListSerializer,
   
    CountryCreateUpdateSerializer, StateCreateUpdateSerializer,
    CityCreateUpdateSerializer, AddressCreateUpdateSerializer
)


class CountryViewSet(BaseViewSet,viewsets.ModelViewSet):
    
    queryset = Country.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CountryListSerializer
        return CountryCreateUpdateSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def lookup(self, request):
        countries = Country.objects.filter(is_active=True).order_by('name')
        serializer = CountryListSerializer(countries, many=True)
        
        return Response({
            'success': True,
            'count': countries.count(),
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def search(self, request):
        query = request.query_params.get('q', '').strip()
        
        if not query:
            return Response({
                'success': False,
                'message': 'Search query is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        countries = Country.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query),
            is_active=True
        )[:20]
        
        serializer = CountryListSerializer(countries, many=True)
        
        return Response({
            'success': True,
            'count': countries.count(),
            'data': serializer.data
        })

class StateViewSet(BaseViewSet,viewsets.ModelViewSet):
    queryset = State.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'country__name']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return StateListSerializer
        return StateCreateUpdateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        country_id = self.request.query_params.get('country_id')
        
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def lookup(self, request):
        country_id = request.query_params.get('country_id')
        
        if not country_id:
            return Response({
                'success': False,
                'message': 'country_id parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        states = State.objects.filter(
            country_id=country_id,
            is_active=True
        ).order_by('name')
        
        serializer = StateListSerializer(states, many=True)
        
        return Response({
            'success': True,
            'count': states.count(),
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='by-country/(?P<country_id>[^/.]+)')
    def by_country(self, request, country_id=None):
        
        country = get_object_or_404(Country, id=country_id)
        states = State.objects.filter(country=country, is_active=True).order_by('name')
        
        serializer = StateListSerializer(states, many=True)
        
        return Response({
            'success': True,
            'country': CountryListSerializer(country).data,
            'count': states.count(),
            'data': serializer.data
        })

class CityViewSet(BaseViewSet,viewsets.ModelViewSet):
    queryset = City.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'state__name', 'state__country__name']
    ordering_fields = ['name', 'code']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CityListSerializer
        return CityCreateUpdateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        state_id = self.request.query_params.get('state_id')
        country_id = self.request.query_params.get('country_id')
        
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        elif country_id:
            queryset = queryset.filter(state__country_id=country_id)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def lookup(self, request):
        state_id = request.query_params.get('state_id')
        
        if not state_id:
            return Response({
                'success': False,
                'message': 'state_id parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cities = City.objects.filter(
            state_id=state_id,
            is_active=True
        ).order_by('name')
        
        serializer = CityListSerializer(cities, many=True)
        
        return Response({
            'success': True,
            'count': cities.count(),
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='by-state/(?P<state_id>[^/.]+)')
    def by_state(self, request, state_id=None):
       
        state = get_object_or_404(State, id=state_id)
        cities = City.objects.filter(state=state, is_active=True).order_by('name')
        
        serializer = CityListSerializer(cities, many=True)
        
        return Response({
            'success': True,
            'state': StateListSerializer(state).data,
            'count': cities.count(),
            'data': serializer.data
        })

class AddressViewSet(BaseViewSet,viewsets.ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AddressListSerializer
        return AddressCreateUpdateSerializer
    
    def get_queryset(self):
        user_profile = self.request.user.profiles.first()
        if user_profile and user_profile.address:
            return Address.objects.filter(id=user_profile.address.id)
        return Address.objects.none()
    
    @action(detail=False, methods=['get'], url_path='my-address')
    def my_address(self, request):
        
        user_profile = request.user.profiles.first()
        
        if not user_profile or not user_profile.address:
            return Response({
                'success': True,
                'message': 'No address found',
                'data': None
            })
        
        serializer = AddressListSerializer(user_profile.address)
        
        return Response({
            'success': True,
            'message': 'Address retrieved successfully',
            'data': serializer.data
        })