```python
import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, HttpResponseTooManyRequests
from django.conf import settings


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
    en dehors de la plage 06h00 - 21h00.
    Vérifie aussi s’il est bien configuré dans settings.py
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # Vérification configuration
        middleware_path = "chats.middleware.RestrictAccessByTimeMiddleware"
        if middleware_path not in getattr(settings, "MIDDLEWARE", []):
            raise Exception(
                f"settings.py doesn't contain: ['{middleware_path}']"
            )

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Autoriser uniquement entre 6h00 et 21h00
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Chat access is restricted between 9PM and 6AM.</p>"
            )

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware qui limite le nombre de messages envoyés
    par chaque IP à 5 par minute (rate limiting).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionnaire {ip: [timestamps]}
        self.message_logs = {}

    def __call__(self, request):
        # Vérifier uniquement les requêtes POST sur /chats (envoi message)
        if request.method == "POST" and "/chats" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialiser la liste pour cette IP si inexistante
            if ip not in self.message_logs:
                self.message_logs[ip] = []

            # Nettoyer les anciennes requêtes (> 1 min)
            one_minute_ago = now - timedelta(minutes=1)
            self.message_logs[ip] = [
                ts for ts in self.message_logs[ip] if ts > one_minute_ago
            ]

            # Vérifier la limite
            if len(self.message_logs[ip]) >= 5:
                return HttpResponseTooManyRequests(
                    "<h1>429 Too Many Requests</h1><p>You can only send 5 messages per minute.</p>"
                )

            # Ajouter la nouvelle requête
            self.message_logs[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """ Récupère l’adresse IP du client """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip
```
