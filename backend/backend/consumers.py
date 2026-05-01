import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Room group mein join karein
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Room group se nikal jayein
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Jab Frontend se message aaye
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']

        # Yahan aap chahein toh database mein message save kar sakte hain

        # Room group ko message bhejein
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            }
        )

    # Message jo group se receive hoga aur har connected client ko jayega
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        # WebSocket ko data bhejein
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))