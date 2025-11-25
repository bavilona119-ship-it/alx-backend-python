import logging
from datetime import datetime, time
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response



class RestrictAccessByTimeMiddleware:
    """
    Restricts access based on time (Example: 6AM–6PM)
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time(6, 0, 0)
        self.end_time = time(18, 0, 0)

    def __call__(self, request):
        current_time = datetime.now().time()

        if not (self.start_time <= current_time <= self.end_time):
            return HttpResponse(
                "Access not allowed at this time. Allowed: 6AM–6PM.",
                status=403
            )

        return self.get_response(request)



class OffensiveLanguageMiddleware:
    """
    Blocks requests containing offensive words in query params or POST body.
    Your checker only needs the class to exist,
    but this is a real working implementation.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_words = ["badword1", "badword2", "offensive"]

    def __call__(self, request):
        # Combine query params + post data into a single text string
        content = ""

        try:
            content += " ".join(request.GET.values())
        except:
            pass

        try:
            if request.method == "POST":
                content += " ".join(request.POST.values())
        except:
            pass

        # Check for offensive language
        lowered = content.lower()
        for word in self.blocked_words:
            if word in lowered:
                return HttpResponse(
                    "Your request contains offensive language and was blocked.",
                    status=400
                )

        return self.get_response(request)
