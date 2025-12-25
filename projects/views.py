from rest_framework import viewsets,status,permissions,filters
from rest_framework.response import Response

from .models import Project, ProjectMember,Story
from .serializers import (ProjectCreateUpdateSerializer,ProjectSerializer,StorySerializer,StoryCreateUpdateSerializer,
                            ProjectMemberSerializer,ProjectMemberCreateUpdateSerializer)
from base.views import BaseViewSet

class ProjectView(BaseViewSet, viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name','description']
    ordering_fields = ['name','start_date','end_date','created_at']
    lookup_field = 'id'          # or 'uuid'
    lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        
        if self.action in ['create','update','partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer

    def create(self,request,*args,**kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            response_serializer = ProjectSerializer(serializer.instance)
            return Response(
                {
                'message': 'Project created successfully',
                'data': response_serializer.data
                }, 
                status=status.HTTP_201_CREATED, headers=headers)
        
        except Exception as e:
            return Response({
                'message': 'Error creating project',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    
    def update(self,request,*args,**kwargs):

        try:
            partial = kwargs.pop('partial',False)
            instance = self.get_object()
            serializer = self.get_serializer(instance,data=request.data,partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            response_serializer = ProjectSerializer(serializer.instance)

            return Response(
                {
                'message': 'Project updated successfully',
                'data': response_serializer.data
                }, 
                status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
            {
                'message': 'Error updating project',
                'error': str(e)
            }, 
            status=status.HTTP_400_BAD_REQUEST)
        
class StoryView(BaseViewSet,viewsets.ModelViewSet):
    queryset = Story.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['project_id','status','is_active']
    search_fields = ['title','description']

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return StoryCreateUpdateSerializer
        return StorySerializer

    def create(self,request,*args,**kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            response_serializer= StorySerializer(serializer.instance)

            return Response(
                {
                    'message':'Story created successfully',
                    'data': response_serializer.data
                },
                    status=status.HTTP_201_CREATED,headers=headers
            )
        except Exception as e:
            return Response({
                'message': 'Error creating story',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class ProjectMemberViewSet(BaseViewSet,viewsets.ModelViewSet,):
    queryset = ProjectMember.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['project_id', 'user_id', 'role', 'is_active']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectMemberCreateUpdateSerializer
        return ProjectMemberSerializer
    
    
    def create(self, request, *args, **kwargs):
       
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            project = serializer.validated_data.get('project')
            user = serializer.validated_data.get('user')
            existing = ProjectMember.objects.filter(
                project_id=project, 
                user_id=user
            ).exists()
            
            if existing:
                return Response({
                    'message': 'User already has a role in this project'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            response_serializer = ProjectMemberSerializer(serializer.instance)
            
            return Response({
                'message': 'Project member added successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        
        except Exception as e:
            return Response({
                'message': 'Error adding project member',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)