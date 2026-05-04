from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Follow
from django.contrib.auth import get_user_model
from notification.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()

class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        
        if request.user == target_user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already following
        follow_obj = Follow.objects.filter(follower=request.user, following=target_user)

        if follow_obj.exists():
            # UNFOLLOW LOGIC
            follow_obj.delete()
            
            Notification.objects.filter(
                recipient=target_user, 
                sender=request.user, 
                notification_type='follow_request'
            ).delete()
            
            return Response({"message": "Unfollowed successfully", "is_following": False}, status=status.HTTP_200_OK)
            
        else:
            Follow.objects.create(follower=request.user, following=target_user)
            
            # --- NOTIFICATION LOGIC START ---
            Notification.objects.create(
                recipient=target_user,
                sender=request.user,
                notification_type='follow_request'
            )

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
            # --- NOTIFICATION LOGIC END ---

            return Response({"message": "Followed successfully", "is_following": True}, status=status.HTTP_201_CREATED)