from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    """
    ✅ Modèle principal pour la messagerie
    - Support des threads (parent_message)
    - Suivi d’édition (edited)
    - Indicateur de lecture (unread)
    - Manager personnalisé pour messages non lus
    """

    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # ✅ champ pour indiquer si le message est non lu
    unread = models.BooleanField(default=True)

    # ✅ relation pour threaded messages
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE
    )

    # ✅ managers
    objects = models.Manager()
    unread_messages = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    def mark_as_read(self):
        """Marque le message comme lu"""
        self.unread = False
        self.save(update_fields=['unread'])
