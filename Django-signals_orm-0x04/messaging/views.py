from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message


@login_required
def unread_inbox(request):
    """
    ✅ Vue pour afficher uniquement les messages non lus de l'utilisateur connecté.
    Utilise le manager personnalisé et .only() pour optimisation.
    """
    user = request.user
    unread_messages = Message.unread_messages.unread_for_user(user)  # utilisation du custom manager

    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})


@login_required
@cache_page(60)  # ✅ Vue mise en cache pour 60 secondes
def conversation_view(request, username):
    """
    ✅ Vue pour afficher une conversation complète (déjà mise en cache)
    """
    from django.contrib.auth.models import User
    from django.db.models import Prefetch

    other_user = User.objects.get(username=username)
    user = request.user

    messages = (
        Message.objects.filter(sender__in=[user, other_user], receiver__in=[user, other_user])
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related(Prefetch('replies'))
        .only('id', 'sender__username', 'receiver__username', 'content', 'timestamp')  # ✅ optimisation .only()
        .order_by('timestamp')
    )

    return render(request, 'messaging/conversation.html', {'messages': messages, 'other_user': other_user})
