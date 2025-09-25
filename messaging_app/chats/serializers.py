# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message


# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    # Exemple d'utilisation de serializers.CharField explicitement
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
            "full_name",
        ]


# -------------------------
# Message Serializer
# -------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # Exemple d'utilisation de SerializerMethodField
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "preview",
            "sent_at",
        ]

    def get_preview(self, obj):
        """Retourne un extrait du message (50 caractères max)."""
        return obj.message_body[:50] + ("..." if len(obj.message_body) > 50 else "")


# -------------------------
# Conversation Serializer
# -------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]

    def validate(self, data):
        """
        Exemple d'utilisation de ValidationError :
        On empêche la création d'une conversation sans participants.
        """
        if not self.instance and not data.get("participants"):
            raise serializers.ValidationError("Une conversation doit avoir au moins un participant.")
        return data
