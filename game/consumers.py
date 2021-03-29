import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async

"""
Временно смешаю логику и консьюмеры,
после написания будет понимание что и куда пихать,
Что можно выделить, а что нет
"""
class GameConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_player_of_user(self):
        player_instance = self.scope['user'].player.first()
        if not player_instance:
            return None
        return player_instance.session.get().id

    async def connect(self):
        # Reg user for send message if close
        self.room_name = 'user_{}'.format(self.scope['user'].id if self.scope['user'].is_authenticated else 'anon')
        self.room_group_name = 'session_%s' % self.room_name
        # Join room group
        print(self.scope['session'],self.scope['user'])
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        if self.scope['user'].is_anonymous:
            print('not auth')
            await self.send(text_data=json.dumps({'data':{'error': 'Not authenticated!'}}), close=True)


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.send(text_data=json.dumps({'data':{'message': 'Close channel'}}), close=True)



    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
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
