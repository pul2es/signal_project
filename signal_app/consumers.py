# signal_app/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Signal, UserSignal
from django.utils import timezone

class SignalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.game_type = self.scope['url_route']['kwargs']['game_type']
        
        await self.channel_layer.group_add(
            f"signal_{self.game_type}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"signal_{self.game_type}",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'get_signal':
            signal = await self.generate_new_signal()
            await self.send(text_data=json.dumps({
                'action': 'new_signal',
                'signal': {
                    'value': str(signal.value),
                    'expires_at': signal.expires_at.timestamp()
                }
            }))

    @database_sync_to_async
    def generate_new_signal(self):
        return Signal.generate_signal(self.game_type)

    async def signal_update(self, event):
        await self.send(text_data=json.dumps(event))