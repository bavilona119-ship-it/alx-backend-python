from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    ✅ Avant modification d’un message : enregistre l’ancien contenu dans MessageHistory.
    """
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    ✅ Lorsqu’un nouveau Message est créé → créer une Notification pour le destinataire.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"Nouveau message de {instance.sender.username}"
        )


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    ✅ Nettoyage automatique des données liées quand un utilisateur est supprimé.
    """
    try:
        Message.objects.filter(sender=instance).delete()
        Message.objects.filter(receiver=instance).delete()
        MessageHistory.objects.filter(edited_by=instance).delete()
        Notification.objects.filter(user=instance).delete()
    except Exception as e:
        print(f"Erreur lors du nettoyage pour {instance}: {e}")
