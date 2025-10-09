from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    ✅ Custom manager pour filtrer les messages non lus d'un utilisateur.
    Utilise .only() pour optimiser la requête (charger uniquement les champs nécessaires).
    """

    def unread_for_user(self, user):
        return (
            self.filter(receiver=user, unread=True)
            .select_related('sender')
            .only('id', 'sender__username', 'content', 'timestamp')
            .order_by('-timestamp')
        )
