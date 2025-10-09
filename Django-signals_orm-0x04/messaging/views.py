from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch
from django.contrib.auth.models import User
from .models import Message


@login_required
def unread_inbox(request):
    """
    ✅ Vue affichant uniquement les messages non lus de l'utilisateur connecté.
    Utilise le custom manager et .only() pour optimiser la requête.
    """
    user = request.user
    unread_messages = Message.unread_messages.unread_for_user(user)
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})


@login_required
@cache_page(60)  # ✅ Cache la vue pendant 60 secondes
def conversation_view(request, username):
    """
    ✅ Vue qui affiche la conversation entre l'utilisateur connecté et un autre.
    - Utilise select_related et prefetch_related pour optimisation ORM
    - Filtre les messages envoyés par request.user
    """

    other_user = get_object_or_404(User, username=username)
    user = request.user

    # ✅ Optimisation des requêtes
    messages = (
        Message.objects.filter(
            sender__in=[user, other_user],
            receiver__in=[user, other_user],
            sender=request.user  # ✅ filtrage par l'utilisateur actuel
        )
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
        .only('id', 'sender__username', 'receiver__username', 'content', 'timestamp')
        .order_by('timestamp')
    )

    return render(request, 'messaging/conversation.html', {
        'messages': messages,
        'other_user': other_user,
    })
