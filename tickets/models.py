from django.db import models
from django.contrib.auth import get_user_model

from base.models import BaseModel
from projects.models import Story, ProjectMember,Project

class Ticket(BaseModel):
    story_id = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_member_id = models.ForeignKey(ProjectMember, on_delete=models.CASCADE, related_name='assigned_member')
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    due_date = models.DateField()   

class TicketComment(BaseModel):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()

class TicketHistory(BaseModel):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='histories')
    field_changed = models.CharField(max_length=50)
    old_value = models.CharField(max_length=100)
    new_value = models.CharField(max_length=100)

class TicketAttachment(BaseModel):
    file = models.FileField(upload_to='ticket_attachments/')
    comment_id = models.ForeignKey(TicketComment, on_delete=models.CASCADE, related_name='attachments')
    
    