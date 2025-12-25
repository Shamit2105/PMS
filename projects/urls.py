from django.urls import path,include 
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import StoryView,ProjectView,ProjectMemberViewSet



router = DefaultRouter()
router.register(r'projects',ProjectView,basename='project')

projects_router = NestedDefaultRouter(router,r'projects',lookup = 'project')
projects_router.register(r'stories',StoryView,basename='project-stories')
projects_router.register(r'project-members',ProjectMemberViewSet,basename='projectmember')

urlpatterns=[
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
]