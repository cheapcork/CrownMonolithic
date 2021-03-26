# from channels import Group
#
#
# def ws_connect(message):
#     Group('users').add(message.reply_channel)
#
#
# def ws_disconnect(message):
#     Group('users').discard(message.reply_channel)


# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['headers'], self.scope['user'])

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'session_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(self.channel_name)
        # Send message to room group
        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))