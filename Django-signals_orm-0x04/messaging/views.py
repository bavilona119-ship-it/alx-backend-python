from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Message, Notification


@login_required
@cache_page(60)  # ✅ mise en cache de la vue de conversation (tâche 5)
def conversation_view(request, username):
    """
    ✅ Affiche la conversation entre l'utilisateur connecté et `username`.
    - Utilise select_related et prefetch_related pour optimiser les requêtes
    - Récupère aussi les réponses (threaded messages)
    """
    other_user = get_object_or_404(User, username=username)
    user = request.user

    # ✅ Filtrer les messages entre les deux utilisateurs
    messages_qs = (
        Message.objects.filter(
            sender__in=[user, other_user],
            receiver__in=[user, other_user]
        )
        .select_related('sender', 'receiver', 'parent_message')  # optimisation
        .prefetch_related('replies')  # optimisation
        .order_by('timestamp')
    )

    # ✅ Récupération récursive des réponses pour afficher le thread complet
    def get_replies(message):
        replies = message.replies.select_related('sender', 'receiver')
        all_replies = []
        for reply in replies:
            all_replies.append(reply)
            all_replies.extend(get_replies(reply))
        return all_replies

    threaded_messages = []
    for msg in messages_qs.filter(parent_message__isnull=True):
        msg.all_replies = get_replies(msg)
        threaded_messages.append(msg)

    context = {
        "messages": threaded_messages,
        "other_user": other_user,
    }
    return render(request, "messaging/conversation.html", context)


@login_required
def inbox_view(request):
    """
    ✅ Affiche les messages non lus de l'utilisateur connecté.
    Utilise .only() pour optimiser la récupération des champs.
    """
    unread_messages = Message.unread_messages.unread_for_user(request.user).only(
        "id", "sender", "receiver", "content", "timestamp"
    )
    return render(request, "messaging/inbox.html", {"messages": unread_messages})


@login_required
def delete_user(request):
    """
    ✅ Vue pour permettre à l'utilisateur de supprimer son compte.
    """
    user = request.user
    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"Le compte '{username}' a été supprimé avec succès.")
        return redirect("home")
    return redirect("profile")


@login_required
def notifications_view(request):
    """
    ✅ Liste les notifications de l'utilisateur connecté.
    """
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "messaging/notifications.html", {"notifications": notifications})
