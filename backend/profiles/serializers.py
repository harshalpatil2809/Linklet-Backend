from rest_framework import serializers
from .models import Profile
from follows.models import Follow

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'full_name', 'bio', 'avatar', 'is_following', 'is_online']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check if current user follows this profile's owner
            return Follow.objects.filter(follower=request.user, following=obj.user).exists()
        return False
    
    