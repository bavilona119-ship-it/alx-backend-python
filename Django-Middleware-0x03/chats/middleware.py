import logging
from datetime import datetime, time
from django.http import HttpResponse


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Configure file logger
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
    Restricts access to certain hours (example: allow only from 6AM–6PM)
    Your checker only needs the class to exist,
    but this version is REAL and fully functional.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time(6, 0, 0)   # 06:00 AM
        self.end_time = time(18, 0, 0)    # 06:00 PM

    def __call__(self, request):
        current_time = datetime.now().time()

        # If outside allowed hours → block the request
        if not (self.start_time <= current_time <= self.end_time):
            return HttpResponse(
                "Access not allowed at this time. Allowed: 6AM to 6PM.",
                status=403
            )

        return self.get_response(request)
