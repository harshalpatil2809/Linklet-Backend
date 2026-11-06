from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Follow
from django.contrib.auth import get_user_model
from notification.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.cache.invalidation import (
    invalidate_follow_cache,
    invalidate_target_profile_cache,
    invalidate_notification_cache,
)
from django.db import transaction

User = get_user_model()

class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def invalidate_related_cache(self, requester, target_user):
        def invalidate():
            # Invalidate follow lists for both users
            invalidate_follow_cache(requester.id)
            invalidate_follow_cache(target_user.id)

            # Invalidate target profile cache for requester
            invalidate_target_profile_cache(
                requester.id,
                target_user.username
            )

            # Invalidate target user's notification history
            invalidate_notification_cache(target_user.id)

        transaction.on_commit(invalidate)

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)

        if request.user == target_user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow_obj = Follow.objects.filter(
            follower=request.user,
            following=target_user
        )

        if follow_obj.exists():
            # UNFOLLOW
            follow_obj.delete()

            Notification.objects.filter(
                recipient=target_user,
                sender=request.user,
                notification_type='follow_request'
            ).delete()

            self.invalidate_related_cache(request.user, target_user)

            return Response(
                {
                    "message": "Unfollowed successfully",
                    "is_following": False
                },
                status=status.HTTP_200_OK
            )

        # FOLLOW
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )

        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type='follow_request'
        )

        self.invalidate_related_cache(request.user, target_user)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'notify_{target_user.id}',
            {
                'type': 'send_notification',
                'notification_type': 'follow_request',
                'message': f"{request.user.username} started following you.",
                'sender_id': request.user.id,
                'sender_username': request.user.username
            }
        )

        return Response(
            {
                "message": "Followed successfully",
                "is_following": True
            },
            status=status.HTTP_201_CREATED
        )