import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import User, Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.user = None
        self.receiver = None
        self.receiver_notificator = None

    async def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % room_name
        self.user = self.scope['user']
        self.receiver = User.objects.get(
            pk=[int(i) for i in room_name.split('-') if i.isnumeric() and int(i) != self.user.pk][0]
        )
        self.receiver_notificator = 'notificator_%d' % self.receiver.id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_notification',
                'notification': "%s join the chat" % self.user
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_notification',
                'notification': "%s left this chat" % self.user
            }
        )
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        from_user = text_data_json['from']
        to_user = text_data_json['to']

        ms = Message(message=message, from_user_id=from_user, to_user_id=to_user)
        ms.save()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_id': ms.id,
                'from_user': from_user,
                'to_user': to_user,
                'time': ms.time.strftime("%H:%m")
            }
        )
        await self.channel_layer.group_send(
            self.receiver_notificator,
            {
                'type': 'notificator_update',
                'user': from_user,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        if self.user.id == event['to_user']:
            Message.objects.filter(id__exact=event['message_id']).update(read=True)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    async def chat_notification(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))


class UserConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = None
        self.notificator = None
        self.user = None

    async def connect(self):
        self.name = self.scope['url_route']['kwargs']['customer_name']
        self.notificator = 'notificator_%s' % self.name
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.notificator,
            self.channel_name
        )

        await self.accept()

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        text_data_json.update({'type': 'notificator_update'})
        await self.channel_layer.group_send(
            self.notificator,
            text_data_json
        )

    # Receive message from room group
    async def notificator_update(self, event):
        await self.send(text_data=json.dumps(event))
