from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import TicketViewSet,TicketCommentView,TicketAttachmentView

router = DefaultRouter()
router.register(r'tickets',TicketViewSet,basename='ticket')
router.register(r'ticketComments',TicketCommentView,basename='ticket_comment')
router.register(r'ticketAttachments',TicketAttachmentView,basename='ticket_attachment')

urlpatterns=[
    path('',include(router.urls))
]