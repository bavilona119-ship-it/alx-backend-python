# chats/permissions.py
from rest_framework import permissions  # ✅ attendu par le checker

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Autoriser seulement les utilisateurs authentifiés qui participent
    à une conversation à voir, envoyer, modifier ou supprimer des messages.
    """

    def has_permission(self, request, view):
        # Autoriser seulement si l'utilisateur est authentifié
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Vérifie que l'utilisateur est bien un participant de la conversation.
        Supposons que le modèle Message a une relation "conversation"
        et que Conversation a un ManyToManyField "participants".
        """
        return request.user in obj.conversation.participants.all()

