```python
import logging
from datetime import datetime
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    """
    Middleware qui enregistre chaque requête utilisateur
    dans un fichier requests.log
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Configuration du logger
        logging.basicConfig(
            filename="requests.log",  # Fichier log dans le répertoire racine du projet
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware qui bloque l’accès aux chats
    en dehors de la plage 06h00 - 21h00
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Autoriser uniquement entre 6h00 et 21h00
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Chat access is restricted between 9PM and 6AM.</p>"
            )

        response = self.get_response(request)
        return response
```
