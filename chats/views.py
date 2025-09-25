from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """
        Endpoint: /conversations/<id>/add_message/
        Permet d’envoyer un message dans une conversation existante
        """
        conversation = self.get_object()
        sender = request.user  # l’utilisateur connecté
        message_body = request.data.get("message_body")

        if not message_body:
            return Response({"error": "Message body is required"}, status=400)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        return Response(MessageSerializer(message).data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
