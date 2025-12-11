from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(to=get_user_model(),null=True,blank=True,on_delete=models.SET_NULL
                                   ,related_name='%(class)s_created',)
    updated_by = models.ForeignKey(to=get_user_model(),null=True,blank=True,on_delete=models.SET_NULL,
                                   related_name='%(class)s_updated')
    is_active = models.BooleanField(default=True,)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)
