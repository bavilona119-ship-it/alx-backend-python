from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def delete_user(request):
    """
    ✅ Permet à un utilisateur connecté de supprimer son compte.
    Le signal post_delete s'occupera du nettoyage automatique.
    """
    user = request.user
    user.delete()  # 🔹 Déclenche automatiquement le signal post_delete
    return redirect('home')  # ou la page d’accueil après suppression
