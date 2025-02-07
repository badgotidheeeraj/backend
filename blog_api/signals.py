from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserActivityLog


# add this into main
@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action="User logged in",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action="User logged out",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )
