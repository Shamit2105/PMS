from rest_framework import viewsets,status,permissions,filters
from rest_framework.response import Response



from .models import Ticket,TicketComment,TicketAttachment
from .serializers import (TicketCreateUpdateSerializer,TicketSerializer,TicketCommentCreateUpdateSerializer,TicketCommentSerializer
            ,TicketAttachmentCreateUpdateSerializer,TicketAttachmentSerializer)
from base.views import BaseViewSet


class TicketViewSet(BaseViewSet,viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    
    filterset_fields = ['status','is_active']
    search_fields = ['name','description']
    ordering_fields = ['name','start_date','end_date','created_at']

    def get_serializer_class(self):
        if self.action in ['create','update']:
            return TicketCreateUpdateSerializer
        return TicketSerializer
        
    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        story_id = self.kwargs.get('story_pk')

        return Ticket.objects.filter(
            story_id=story_id,
            story__project_id=project_id
        )
    
    def create(self,request,*args,**kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_serializer = TicketSerializer(serializer.instance)
            return Response(
                data={
                    'message': 'Project created successfully',
                    'data': response_serializer.data
                }, 
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response({
                'message': 'Error creating project',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class TicketCommentView(BaseViewSet,viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name','description']
    ordering_fields = ['name','start_date','end_date','created_at']


    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_pk')
        return TicketComment.objects.filter(ticket_id=ticket_id)

    def get_serializer_class(self):
        if self.action in ['create','update']:
            return TicketCommentCreateUpdateSerializer
        return TicketCommentSerializer
    
    def create(self, request, *args, **kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_serializer = TicketCommentSerializer(serializer.instance)
            return Response({
                'message': 'Project created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'message': 'Error creating project',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class TicketAttachmentView(BaseViewSet,viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name','description']
    ordering_fields = ['name','start_date','end_date','created_at']

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_pk')
        return TicketAttachment.objects.filter(comment__ticket_id=ticket_id)



    def get_serializer_class(self):
        if self.action in ['create','update']:
            return TicketAttachmentCreateUpdateSerializer
        return TicketAttachmentSerializer
    
    def create(self, request, *args, **kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_serializer = TicketAttachmentSerializer(serializer.instance)
            return Response({
                'message': 'Project created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'message': 'Error creating project',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
