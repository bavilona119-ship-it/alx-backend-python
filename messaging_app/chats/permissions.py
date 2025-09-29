# chats/permissions.py
from rest_framework import permissions  # ✅ attendu par le checker

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission pour autoriser uniquement les participants d'une conversation
    à envoyer, voir, mettre à jour ou supprimer des messages.
    """

    def has_permission(self, request, view):
        # L'utilisateur doit être authentifié
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Vérifie que l'utilisateur est un participant de la conversation.
        """
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()
        return False
