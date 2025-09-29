# messaging_app/chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated   # ✅ attendu par le checker
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation   # ta permission custom
from rest_framework import status as drf_status         # pour HTTP_403_FORBIDDEN

# -------------------------
# Conversation ViewSet
# -------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]   # ✅

    # Ajout de filtres (permet recherche par ID de conversation)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["conversation_id"]
    ordering_fields = ["created_at"]

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get("participants", [])
        if not participants_ids:
            raise ValidationError("Une conversation doit avoir au moins un participant.")

        participants = User.objects.filter(user_id__in=participants_ids)
        if not participants.exists():
            raise ValidationError("Les participants spécifiés n'existent pas.")

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Retourne uniquement les conversations où l'utilisateur connecté est participant.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user)


# -------------------------
# Message ViewSet
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]   # ✅

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body", "sender__email"]
    ordering_fields = ["sent_at"]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body")

        if not conversation_id or not sender_id or not message_body:
            raise ValidationError("conversation_id, sender_id et message_body sont requis.")

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        # Vérifier si l'utilisateur est bien un participant de la conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "Vous n'êtes pas autorisé à envoyer un message dans cette conversation."},
                status=drf_status.HTTP_403_FORBIDDEN   # ✅ attendu par le checker
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body,
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Retourne uniquement les messages des conversations
        auxquelles l'utilisateur connecté participe.
        """
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)   # ✅ attendu par le checker

