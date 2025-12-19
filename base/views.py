from django.shortcuts import render

from django.conf import settings
from django.db import transaction
from django.http import Http404
from rest_framework import viewsets,status,filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class BaseViewSet(viewsets.GenericViewSet):
    ordering = ('-created_at',)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    

    def perform_update(self,serializer):
        serializer.save(updated_by=self.request.user)
        
        