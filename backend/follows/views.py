from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        
        if request.user == target_user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already following
        follow_obj = Follow.objects.filter(follower=request.user, following=target_user)

        if follow_obj.exists():
            follow_obj.delete()
            return Response({"message": "Unfollowed successfully", "is_following": False}, status=status.HTTP_200_OK)
        else:
            Follow.objects.create(follower=request.user, following=target_user)
            return Response({"message": "Followed successfully", "is_following": True}, status=status.HTTP_201_CREATED)