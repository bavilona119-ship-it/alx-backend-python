class RolepermissionMiddleware:
    """
    Middleware qui vérifie le rôle de l’utilisateur avant d’autoriser certaines actions.
    - Autorise uniquement les users avec role 'admin' ou 'moderator'
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exemple : on protège toutes les actions sous /chats/admin/
        if request.path.startswith("/chats/admin") or request.path.startswith("/chats/moderate"):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>You must be logged in to access this resource.</p>"
                )
            # Vérifier le champ role
            user_role = getattr(user, "role", "user")  # fallback = user
            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>Access denied. Only admins and moderators are allowed.</p>"
                )

        response = self.get_response(request)
        return response
