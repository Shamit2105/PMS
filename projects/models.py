from django.db import models
from django.contrib.auth import get_user_model

from base.models import BaseModel

class Project(BaseModel):

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'Projects'

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'



class ProjectMember(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='project_members')
    role = models.CharField(max_length=50)

    class Meta:
        db_table = 'Project_Members'

        verbose_name = 'Project Member'
        verbose_name_plural = 'Project Members'

class Story(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'Project_Stories'

        verbose_name = 'Project Story'
        verbose_name_plural = 'Project Stories'
