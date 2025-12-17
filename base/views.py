from django.shortcuts import render

from django.conf import settings
from django.db import transaction
from django.http import Http404
from rest_framework import viewsets,status,filters
from rest_framework.response import Response

class BaseViewSet(viewsets.GenericViewSet):
    ordering = ('created_at',)
    
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        if "serializer_class" in kwargs:
            serializer_class = kwargs.pop("serializer_class")
        else:
            serializer_class = self.get_serializer_class()
        context = super().get_serializer_context()
        context.update({"request": self.request})
        if 'context' not in kwargs:
            kwargs['context'] = {}
        kwargs['context'].update(context)
        return serializer_class(*args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user,updated_by=self.request.user)
    
    

    def perform_update(self,serializer):
        serializer.save(updated_by=self.request.user)
        
        