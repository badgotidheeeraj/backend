from django.http import JsonResponse
from django.contrib import messages

def get_notifications(request):
    messages.success(request, "New user registered!")
    messages.warning(request, "Server reaching max usage!")
    messages.error(request, "System error detected!")

    notifications = []
    for message in messages.get_messages(request):
        notifications.append({"message": str(message), "type": message.tags})

    return JsonResponse(notifications, safe=False)


# add this code into main module
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserActivityLog
from .serializer import UserActivityLogSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can see logs
def get_user_logs(request):
    logs = UserActivityLog.objects.filter(user=request.user).order_by('-timestamp')
    serializer = UserActivityLogSerializer(logs, many=True)
    return Response(serializer.data)
