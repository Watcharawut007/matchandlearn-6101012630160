import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chatroom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['roomname'] #set a url that must get a request
        self.room_group_name = 'chat_%s' % self.room_name
        if not Chatroom.objects.filter(room_name=self.room_name).exists():#check that chat room is not exist then create chat room model
            Chatroom.objects.create(room_name=self.room_name, user1=self.room_name.split('_')[0],
                                    user2=self.room_name.split('_')[1])#split it for create chat room that user 1 variable contains a username and user 2 too

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

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        adddata = Chatroom.objects.get(room_name=self.room_name)
        adddata.chat += message + "`~`~`~`~`~`"
        adddata.save()

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))