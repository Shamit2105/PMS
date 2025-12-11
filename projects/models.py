from django.db import models
from django.contrib.auth import get_user_model

from base.models import BaseModel

class Project(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)


class ProjectMember(BaseModel):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projects')
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='project_members')
    role = models.CharField(max_length=50)

class Story(BaseModel):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50)


