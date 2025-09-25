# messaging_app/chats/urls.py

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Router principal
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Router imbriqué : messages liés à une conversation
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
