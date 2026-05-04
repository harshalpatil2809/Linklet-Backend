from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_id = serializers.IntegerField(source='sender.id', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 
            'sender_id', 
            'sender_username', 
            'notification_type', 
            'is_read', 
            'created_at'
        ]