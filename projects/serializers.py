from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from datetime import datetime,date

from .models import Project,ProjectMember,Story
from base.serializers import BaseModelSerializer,BaseSerializer

User = get_user_model()

class ProjectMemberSerializer(BaseModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['id', 'project_id', 'user_id', 'role', 'created_at', 
                 'updated_at', 'created_by', 'updated_by', 'is_active']
        read_only_fields = ['id q', 'created_at', 'updated_at', 
                           'created_by', 'updated_by', 'is_active']

class ProjectMemberCreateUpdateSerializer(BaseModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ProjectMember
        fields = ['user','role','project']

    def validate(self,attrs):
        if self.instance:
            project_id = attrs['project']
            user_id = attrs['user']
        else:
            project_id=None
            user_id = attrs['user']
        if project_id and user_id:
            existing = ProjectMember.objects.filter(project=project_id,user=user_id().exclude(pk=getattr(self.instance,'pk',None)))
            if existing.exists():
                raise serializers.ValidationError({'user_id':'This user already has a role in this project'})
        
        valid_roles = ['Manager','BackEndDeveloper','FrontEndDeveloper',]
        role = attrs.get('role',getattr(self.instance,'role',None))
        if role and role not in valid_roles:
            raise serializers.ValidationError({
                'role':f'Role must be one of: {",".join(valid_roles)}'
            })
        return attrs
    
    def create(self, validated_data):
        return super().create(validated_data)
    



class StorySerializer(BaseModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'project_id', 'title', 'description', 'status',
                 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at', 
                           'created_by', 'updated_by', 'is_active']
        
    
class StoryCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Story
        fields = ['project','title','description','status',]
    
    def validate(self,attrs):
        #title = attrs.get('title',getattr(self.instance,'title',''))
        valid_statuses = ['todo', 'in_progress', 'review', 'done', 'blocked']
        status = attrs['status']
        if status and status not in valid_statuses:
            raise serializers.ValidationError({
                'status': f'Status must be one of: {", ".join(valid_statuses)}'
            })
        
        return attrs
    
    def create(self, validated_data):
        return super().create(validated_data)

class ProjectSerializer(BaseModelSerializer):
    stories = StorySerializer(many=True,read_only = True)
    project_members = ProjectMemberSerializer(many=True,read_only=True)
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date', 'status',
            'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active',
            'stories','project_members',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 
                           'created_by', 'updated_by', 'is_active']

class ProjectCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Project
        fields = ['name','description','start_date','end_date','status']

    def validate(self, attrs):
        start_date = attrs.get('start_date') or date.today()
        end_date = attrs.get('end_date')

        if end_date and start_date > end_date:
            raise serializers.ValidationError({
                'end_date': 'End date cannot be before start date'
            })

        return attrs

    def create(self, validated_data):
        validated_data['start_date'] = date.today()

        return super().create(validated_data)
