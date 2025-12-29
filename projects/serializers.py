from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from datetime import datetime,date

from base.models import BaseModel

from .models import Project,ProjectMember,Story
from base.serializers import BaseModelSerializer,BaseSerializer

User = get_user_model()

class ProjectMemberSerializer(BaseModelSerializer):
    user_first_name = serializers.CharField(
        source="user.username", read_only=True
    )
    

    class Meta(BaseModelSerializer.Meta):
        model = ProjectMember
        fields = [
            'id',
            'project',
            'user',
            'user_first_name',
            'role',
            'created_at',
            'updated_at',
            'is_active'
        ]



class ProjectMemberCreateUpdateSerializer(BaseModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta(BaseModelSerializer.Meta):
        model = ProjectMember
        fields = ['user','role','project']

    def validate(self,attrs):
        project= attrs['project']
        user = attrs['user']

        if self.instance: #update going on
            if not project:
                project = self.instance.project
            if not user:
                user = self.instance.user

        if project and user:
            existing = ProjectMember.objects.filter(project=project, user=user)
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise serializers.ValidationError("User already has a role in this project")

    def create(self, validated_data):
        return super().create(validated_data)


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class StorySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Story
        fields = ['id', 'project', 'title', 'description', 'status',
                 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active']



class StoryCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Story
        fields = ['project','title','description','status',]

    def validate(self,attrs):

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
    class Meta(BaseModelSerializer.Meta):
        model = Project
        fields = [
            'name', 'description', 'start_date', 'end_date', 'status',
            'stories','project_members',
        ]


class ProjectCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
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

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        validated_data['start_date'] = date.today()

        project = super().create(validated_data)

        ProjectMember.objects.create(
            project=project,
            user=user,
            role="owner",  
            created_by=user,
            updated_by=user
        )

        return project