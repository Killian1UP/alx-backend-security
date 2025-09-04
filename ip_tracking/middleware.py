from .models import RequestLog

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Capture request details
        ip = request.META.get('REMOTE_ADDR')
        path = request.path

        # Save to the database
        RequestLog.objects.create(ip_address=ip, path=path)

        # Continue to next middleware or view
        response = self.get_response(request)
        return response
