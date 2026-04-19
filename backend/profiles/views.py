from rest_framework import generics, permissions,filters
from .models import Profile
from .serializers import ProfileSerializer
from follows.models import Follow

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


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
        
        my_following = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        
        mutual_user_ids = Follow.objects.filter(
            follower_id__in=my_following, 
            following=user
        ).values_list('follower_id', flat=True)
        
        return Profile.objects.filter(user_id__in=mutual_user_ids)
    



class FollowersListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # 1. Un logo ki IDs nikalo jo "Mujhe" (request.user) follow kar rahe hain
        follower_ids = Follow.objects.filter(following=user).values_list('follower_id', flat=True)
        
        # 2. In IDs ki Profiles return karo
        return Profile.objects.filter(user_id__in=follower_ids)
    

class FollowingListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        return Profile.objects.filter(user_id__in=following_ids)