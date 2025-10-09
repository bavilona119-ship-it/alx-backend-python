from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    """
    ✅ Modèle Message mis à jour :
    - parent_message : pour les réponses en thread
    - unread : pour messages non lus
    - managers personnalisés
    """

    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    unread = models.BooleanField(default=True)

    # ✅ Ajout du champ parent_message (self-referential)
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
        self.unread = False
        self.save(update_fields=['unread'])
