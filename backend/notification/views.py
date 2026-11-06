
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer

from core.cache.keys import notification_history_key
from core.cache.ttl import CacheTTL
from core.cache.services import get_or_set_cached_data


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):

    cache_key = notification_history_key(request.user.id)

    def fetch_notifications():
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by('-created_at')

        serializer = NotificationSerializer(
            notifications,
            many=True
        )

        return list(serializer.data)

    data = get_or_set_cached_data(
        cache_key,
        fetch_notifications,
        CacheTTL.NOTIFICATIONS
    )

    return Response(data)
