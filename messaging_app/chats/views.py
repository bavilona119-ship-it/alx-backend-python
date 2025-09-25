# messaging_app/chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# -------------------------
# Conversation ViewSet
# -------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Créer une nouvelle conversation avec des participants.
        Exemple JSON:
        {
            "participants": [user_id1, user_id2]
        }
        """
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


# -------------------------
# Message ViewSet
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Envoyer un message dans une conversation existante.
        Exemple JSON:
        {
            "conversation_id": "...",
            "sender_id": "...",
            "message_body": "Hello world!"
        }
        """
        conversation_id = request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body")

        if not conversation_id or not sender_id or not message_body:
            raise ValidationError("conversation_id, sender_id et message_body sont requis.")

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
