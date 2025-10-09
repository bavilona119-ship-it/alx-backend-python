from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch
from django.contrib.auth.models import User
from .models import Message

@login_required
@cache_page(60)  # cache-page appliqué avec timeout de 60 secondes
def conversation_view(request, username):
    """
    Affiche la liste des messages d'une conversation entre l'utilisateur connecté
    et l'utilisateur `username`. La réponse HTML est mise en cache pendant 60s.
    """
    other_user = get_object_or_404(User, username=username)
    user = request.user

    # Récupération optimisée des messages de la conversation
    messages = (
        Message.objects.filter(
            sender__in=[user, other_user],
            receiver__in=[user, other_user]
        )
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
        .order_by('timestamp')
    )

    return render(request, 'messaging/conversation.html', {
        'messages': messages,
        'other_user': other_user,
    })
