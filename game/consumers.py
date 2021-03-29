import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from game.models import PlayerModel
"""
Временно смешаю логику и консьюмеры,
после написания будет понимание что и куда пихать,
Что можно выделить, а что нет
"""




class GameConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_session_of_user(self):
        try:
            player_instance = self.scope['user'].player.get()
            print(self.scope['user'])
            print(player_instance.session)
        except PlayerModel.DoesNotExist:
            return None
        return player_instance.session.id

    async def connect(self):
        # Reg user for send message if close
        self.room_name = 'user_{}'.format(self.scope['user'].id if self.scope['user'].is_authenticated else 'anon')

        await self.accept()
        if self.scope['user'].is_anonymous:
            print('not auth')
            await self.send(text_data=json.dumps({'data':{'error': 'Not authenticated!'}}), close=True)

        session = await self.get_session_of_user()
        print(session)
        self.room_group_name = 'game_session_{}'.format(session) if session else 'search_for_session'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_group_name, self.room_name)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.send(text_data=json.dumps({'data': {'message': 'Close channel'}}), close=True)



    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['data']
        # await self.channel_layer.send(
        #     self.channel_name,
        #     {
        #         'type': 'sessions1',
        #         'data': message
        #     }
        # )

    # Receive message from room group
    async def sessions(self, event):
        # print(event)
        # sessions = event['sessions']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'data': event['data']
        }))
