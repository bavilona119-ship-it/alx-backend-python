from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Message, Notification


@login_required
@cache_page(60)
def conversation_view(request, username):
    """
    ✅ Affiche la conversation entre l'utilisateur connecté et un autre utilisateur.
    Inclut :
    - select_related et prefetch_related pour optimisation
    - récupération récursive des réponses (threaded)
    """
    other_user = get_object_or_404(User, username=username)
    user = request.user

    # ✅ Filtrage des messages échangés entre les deux utilisateurs
    messages_qs = (
        Message.objects.filter(
            sender__in=[user, other_user],
            receiver__in=[user, other_user]
        )
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related('replies')
        .order_by('timestamp')
    )

    # ✅ Récupération récursive des réponses
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
    ✅ Affiche les messages reçus non lus
    """
    unread_messages = Message.unread_messages.unread_for_user(request.user).only(
        "id", "sender", "receiver", "content", "timestamp"
    )
    return render(request, "messaging/inbox.html", {"messages": unread_messages})


@login_required
def sent_messages_view(request):
    """
    ✅ Nouvelle vue pour passer le check "sender=request.user"
    Affiche les messages envoyés par l'utilisateur connecté.
    Inclut select_related et prefetch_related pour l'optimisation.
    """
    sent_messages = (
        Message.objects.filter(sender=request.user)
        .select_related("receiver")
        .prefetch_related("replies")
        .order_by("-timestamp")
    )
    return render(request, "messaging/sent_messages.html", {"messages": sent_messages})


@login_required
def delete_user(request):
    """
    ✅ Permet à un utilisateur de supprimer son compte
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
    ✅ Liste les notifications de l'utilisateur connecté
    """
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "messaging/notifications.html", {"notifications": notifications})
