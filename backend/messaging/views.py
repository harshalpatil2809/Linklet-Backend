from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer
from follows.models import Follow

User = get_user_model()

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        receiver = get_object_or_404(User, id=user_id)
        sender = request.user

        # 1. Check Mutual Follow
        is_mutual = Follow.objects.filter(follower=sender, following=receiver).exists() and \
                    Follow.objects.filter(follower=receiver, following=sender).exists()
        
        if not is_mutual:
            return Response({"error": "Dono side se follow hona zaroori hai chat ke liye."}, 
                            status=status.HTTP_403_FORBIDDEN)

        # 2. Get or Create Conversation Room
        conversation = Conversation.objects.filter(participants=sender).filter(participants=receiver).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(sender, receiver)

        # 3. Save Message
        text = request.data.get('text')
        if not text:
            return Response({"error": "Message khali nahi ho sakta."}, status=status.HTTP_400_BAD_REQUEST)
            
        message = Message.objects.create(conversation=conversation, sender=sender, text=text)
        
        # Update conversation timestamp for sorting in inbox
        conversation.save() 

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
    



class MessageHistoryView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.kwargs.get('user_id')
        other_user = get_object_or_404(User, id=other_user_id)
    
        conversation = Conversation.objects.filter(
            participants=self.request.user
        ).filter(
            participants=other_user
        ).first()

        if conversation:
            Message.objects.filter(
                conversation=conversation, 
                sender=other_user, 
                is_read=False
            ).update(is_read=True)
        
            return Message.objects.filter(conversation=conversation).order_by('timestamp')
    
        return Message.objects.none()


class InboxListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Sirf wahi conversations dikhao jisme user khud hai
        # updated_at descending taaki latest chat sabse upar aaye
        return Conversation.objects.filter(
            participants=self.request.user
        ).order_by('-updated_at')