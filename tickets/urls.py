from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.routers import DefaultRouter

from projects.views import ProjectView, StoryView
from .views import TicketViewSet, TicketCommentView, TicketAttachmentView

router = DefaultRouter()
router.register(r'projects', ProjectView, basename='project')

projects_router = NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'stories', StoryView, basename='project-stories')

stories_router = NestedDefaultRouter(projects_router, r'stories', lookup='story')
stories_router.register(r'tickets', TicketViewSet, basename='story-tickets')

tickets_router = NestedDefaultRouter(stories_router, r'tickets', lookup='ticket')
tickets_router.register(r'comments', TicketCommentView, basename='ticket-comments')
tickets_router.register(r'attachments', TicketAttachmentView, basename='ticket-attachments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(stories_router.urls)),
    path('', include(tickets_router.urls)),
]
