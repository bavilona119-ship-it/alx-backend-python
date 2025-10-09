from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    """
    ✅ Modèle Message mis à jour :
    - parent_message : pour les réponses en thread
    - unread : pour messages non lus
    - edited/edited_at/edited_by : pour le suivi des modifications
    """

    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ✅ Champs de suivi des modifications
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='edited_messages',
        on_delete=models.SET_NULL
    )

    # ✅ Pour messages non lus
    unread = models.BooleanField(default=True)

    # ✅ Pour les réponses (threaded messages)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    # ✅ Managers
    objects = models.Manager()
    unread_messages = UnreadMessagesManager()

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    def mark_as_read(self):
        """Marque le message comme lu"""
        self.unread = False
        self.save(update_fields=['unread'])


class MessageHistory(models.Model):
    """
    ✅ Historique des modifications de messages :
    Stocke le contenu précédent avant chaque édition.
    """

    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='message_history_edits'
    )

    def __str__(self):
        return f"Historique du message #{self.message.id} à {self.edited_at}"
