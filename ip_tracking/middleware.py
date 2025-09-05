import requests
from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Capture request details
        ip = request.META.get('REMOTE_ADDR')
        path = request.path
        
        # Block if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Forbidden: Your IP has been blocked.")

        # Try to get geolocation from cache
        geo_data = cache.get(ip)
        if not geo_data:
            try:
                response = requests.get(f'https://ipapi.co/{ip}/json/')
                geo_data = response.json()
                # Cache the result for 24 hours (86400 seconds)
                cache.set(ip, geo_data, 86400)
            except requests.exceptions.RequestException:
                geo_data = {}

        country = geo_data.get('country_name', '') if geo_data else ''
        city = geo_data.get('city', '') if geo_data else ''

        # Save to the database
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            country=country,
            city=city
        )

        # Continue to next middleware or view
        response = self.get_response(request)
        return response
