from rest_framework import serializers
from .models import Profile
from follows.models import Follow

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    is_following = serializers.SerializerMethodField()
    # Explicitly avatar field ko handle karein taaki Cloudinary full URL de
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'full_name', 'bio', 'avatar', 'is_following', 'is_online']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Current user aur profile owner ke beech follow relation check karein
            return Follow.objects.filter(follower=request.user, following=obj.user).exists()
        return False

    def to_representation(self, instance):
        """
        Yeh method ensure karega ki avatar ka URL hamesha Full Cloudinary URL ho, 
        na ki local /avatars/ path.
        """
        ret = super().to_representation(instance)
        
        # Agar avatar hai toh uska full URL nikaalein
        if instance.avatar:
            # Cloudinary automatically full URL deta hai .url property par
            ret['avatar'] = instance.avatar.url
        
        # Undefined fix: Agar full_name empty hai toh fallback to username
        if not ret.get('full_name'):
            ret['full_name'] = instance.user.username
            
        return ret