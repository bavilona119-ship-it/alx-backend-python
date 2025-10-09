from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message

# ⚠️ Si tu as aussi un modèle Notification ou MessageHistory, importe-les ici :
# from .models import Notification, MessageHistory


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    ✅ Signal déclenché après la suppression d'un utilisateur.
    Supprime tous les messages, notifications et historiques associés.
    """
    try:
        # Supprimer les messages envoyés ou reçus par l'utilisateur
        Message.objects.filter(sender=instance).delete()
        Message.objects.filter(receiver=instance).delete()

        # ✅ Si tu as des modèles Notification ou MessageHistory :
        # Notification.objects.filter(user=instance).delete()
        # MessageHistory.objects.filter(user=instance).delete()

    except Exception as e:
        print(f"Erreur lors du nettoyage des données liées à {instance}: {e}")
