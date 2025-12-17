from django.urls import path,include 
from rest_framework.routers import DefaultRouter

from .views import StoryView,ProjectView,ProjectMemberViewSet

router = DefaultRouter()
router.register(r'projects',ProjectView,basename='project')
router.register(r'stories',StoryView,basename='story')
router.register(r'project-members',ProjectMemberViewSet,basename='projectmember')

urlpatterns=[
    path('', include(router.urls)),
]