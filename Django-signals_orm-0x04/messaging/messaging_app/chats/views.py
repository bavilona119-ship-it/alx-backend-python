from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from messaging.models import Message


@cache_page(60)  # ✅ Cache cette vue pendant 60 secondes
def conversation_view(request, username):
    """
    ✅ Affiche tous les messages échangés entre l'utilisateur connecté et un autre utilisateur.
    Résultat mis en cache pendant 60 secondes.
    """
    other_user = get_object_or_404(User, username=username)
    user = request.user

    # Optimisation ORM avec select_related et prefetch_related
    messages = (
        Message.objects.filter(
            sender__in=[user, other_user],
            receiver__in=[user, other_user]
        )
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related('replies')
        .order_by('timestamp')
    )

    return render(request, 'chats/conversation.html', {'messages': messages, 'other_user': other_user})
