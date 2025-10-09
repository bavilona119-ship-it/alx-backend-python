from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.auth.models import User


@login_required
def delete_user(request):
    """
    ✅ Vue pour permettre à l'utilisateur de supprimer son propre compte.
    Lors de la suppression, un signal post_delete nettoiera toutes les données liées.
    """
    user = request.user

    if request.method == "POST":
        username = user.username
        user.delete()  # ✅ Supprime l'utilisateur
        messages.success(request, f"Le compte '{username}' a été supprimé avec succès.")
        return redirect('home')  # Redirige vers une page d'accueil ou login

    return redirect('profile')  # Par exemple, si méthode != POST
