from django.db import models
from django.contrib.auth import get_user_model

from base.models import BaseModel
from projects.models import Story, ProjectMember,Project

class Ticket(BaseModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE, related_name='assigned_member')
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    due_date = models.DateField()   

    class Meta:
        db_table = 'Tickets'

        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

class TicketComment(BaseModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()

    class Meta:
        db_table = 'Ticket_Comments'

        verbose_name = 'Ticket Comment'
        verbose_name_plural = 'Ticket Comments'

class TicketHistory(BaseModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='histories')
    field_changed = models.CharField(max_length=50)
    old_value = models.CharField(max_length=100)
    new_value = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ticket_Histories'

        verbose_name = 'Ticket History'
        verbose_name_plural = 'Ticket Histories'

class TicketAttachment(BaseModel):
    file = models.FileField(upload_to='ticket_attachments/')
    comment = models.ForeignKey(TicketComment, on_delete=models.CASCADE, related_name='attachments')

    class Meta:
        db_table = 'Ticket_Attachments'

        verbose_name = 'Ticket Attachment'
        verbose_name_plural = 'Ticket Attachments'
    
    