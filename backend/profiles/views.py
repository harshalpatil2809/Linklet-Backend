from rest_framework import generics, permissions,filters
from .models import Profile
from .serializers import ProfileSerializer
from follows.models import Follow
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from core.cache.keys import my_profile_key
from core.cache.ttl import CacheTTL
from core.cache.services import get_or_set_cached_data
from core.cache.invalidation import invalidate_profile_cache
from core.cache.keys import target_profile_key
from core.cache.ttl import CacheTTL
from core.cache.services import get_or_set_cached_data
from core.cache.keys import (
    mutual_follow_key,
    followers_key,
    following_key,
)
from core.cache.ttl import CacheTTL
from core.cache.services import get_or_set_cached_data

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def retrieve(self, request, *args, **kwargs):
        """
        Return cached profile data when available.
        Otherwise fetch and cache the serialized profile.
        """

        cache_key = my_profile_key(request.user.id)

        profile_data = get_or_set_cached_data(
            cache_key,
            lambda: self.get_serializer(self.get_object()).data,
            CacheTTL.MY_PROFILE,
        )

        return Response(profile_data)

    def perform_update(self, serializer):
        """
        Save profile changes and invalidate the old cached data.
        """

        serializer.save()

        invalidate_profile_cache(self.request.user.id)


class ProfileSearchView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [filters.SearchFilter]
    
    search_fields = ['user__username', 'full_name']

    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user)
    

class MutualFollowListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        my_following = Follow.objects.filter(
            follower=user
        ).values_list('following_id', flat=True)

        mutual_user_ids = Follow.objects.filter(
            follower_id__in=my_following,
            following=user
        ).values_list('follower_id', flat=True)

        return Profile.objects.filter(user_id__in=mutual_user_ids)

    def list(self, request, *args, **kwargs):
        cache_key = mutual_follow_key(request.user.id)

        def fetch_data():
            queryset = self.get_queryset()
            serialized_data = self.get_serializer(queryset, many=True).data
            return [dict(item) for item in serialized_data]

        data = get_or_set_cached_data(
            cache_key,
            fetch_data,
            CacheTTL.MUTUAL_FOLLOW
        )

        return Response(data)


class FollowersListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        follower_ids = Follow.objects.filter(
            following=user
        ).values_list('follower_id', flat=True)

        return Profile.objects.filter(user_id__in=follower_ids)

    def list(self, request, *args, **kwargs):
        cache_key = followers_key(request.user.id)

        def fetch_data():
            queryset = self.get_queryset()
            serialized_data = self.get_serializer(queryset, many=True).data
            return [dict(item) for item in serialized_data]

        data = get_or_set_cached_data(
            cache_key,
            fetch_data,
            CacheTTL.FOLLOWERS
        )

        return Response(data)

class FollowingListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        following_ids = Follow.objects.filter(
            follower=user
        ).values_list('following_id', flat=True)

        return Profile.objects.filter(user_id__in=following_ids)

    def list(self, request, *args, **kwargs):
        cache_key = following_key(request.user.id)

        def fetch_data():
            queryset = self.get_queryset()
            serialized_data = self.get_serializer(queryset, many=True).data
            return [dict(item) for item in serialized_data]

        data = get_or_set_cached_data(
            cache_key,
            fetch_data,
            CacheTTL.FOLLOWERS
        )

        return Response(data)




class TargetUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):

        cache_key = target_profile_key(
            request.user.id,
            username,
        )

        def fetch_profile_data():

            target_profile = get_object_or_404(
                Profile,
                user__username=username,
            )

            is_following = Follow.objects.filter(
                follower=request.user,
                following=target_profile.user,
            ).exists()

            return {
                "id": target_profile.user.id,
                "username": target_profile.user.username,
                "is_following": is_following,
                "bio": target_profile.bio,
                "profile_picture": (
                    target_profile.avatar.url
                    if target_profile.avatar
                    else None
                ),
            }

        profile_data = get_or_set_cached_data(
            cache_key,
            fetch_profile_data,
            CacheTTL.TARGET_PROFILE,
        )

        return Response(profile_data)