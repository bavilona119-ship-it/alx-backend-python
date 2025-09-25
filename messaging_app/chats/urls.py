# messaging_app/chats/urls.py

from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Router principal avec DefaultRouter
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Router imbriqué : messages liés à une conversation
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),              # routes principales
    path('', include(conversations_router.urls)) # routes imbriquées
]
