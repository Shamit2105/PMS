from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from datetime import date

from projects.models import Story,ProjectMember
from base.serializers import BaseModelSerializer,BaseSerializer
from .models import Ticket,TicketAttachment,TicketComment,TicketHistory

User = get_user_model()



class TicketSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Ticket
        fields = ['id','story','title','description','assigned_member','status','priority','type','due_date'
                  ,'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active']
        

class TicketCreateUpdateSerializer(BaseModelSerializer):
    
    class Meta(BaseModelSerializer.Meta):
        model = Ticket
        fields = ['story','title','description','assigned_member','status','priority','type','due_date']

    def validate(self,attrs):
        story_id = attrs['story']
        assigned_member_id = attrs['assigned_member']
        if self.instance:
            if not story_id:
                story_id = self.instance.story
            if not assigned_member_id:
                assigned_member_id = self.assigned_member
        if story_id and assigned_member_id:
            existing = Ticket.objects.filter(story=story_id,assigned_member=assigned_member_id)
            if self.instance:
                existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError("A ticket with same story and same user already exists")
            
        due_date = attrs['due_date']
        if due_date < date.today():
            raise serializers.ValidationError("Due date should be >= today's date")
        return attrs
            
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
class TicketCommentSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = TicketComment
        fields = ['id','ticket','message','created_at', 'updated_at', 'created_by', 'updated_by', 'is_active']
        

class TicketCommentCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = TicketComment
        fields = ['ticket','message']

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
class TicketAttachmentSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = TicketAttachment
        fields= '__all__'
        
class TicketAttachmentCreateUpdateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = TicketComment
        fields = ['file','comment']

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


    