# chats/permissions.py
from rest_framework import permissions   # ✅ obligatoire pour le checker

class IsOwner(permissions.BasePermission):   # ✅ BasePermission bien présent
    """
    Permission pour s'assurer que chaque utilisateur ne peut accéder
    qu'à ses propres messages ou conversations.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'objet (Message ou Conversation) appartient à l'utilisateur connecté
        return obj.user == request.user

