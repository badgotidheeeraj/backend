from django.utils.timezone import now
from .models import UserActivityLog

class TrackUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            UserActivityLog.objects.create(
                user=request.user,
                action=f"API {request.method} request",
                url=request.path,
                method=request.method,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )
        
        return response

    def get_client_ip(self, request):
        """Extracts client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
