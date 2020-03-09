# ebay/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from uuid import uuid4
import time
from django import *
from channels.auth import AuthMiddlewareStack
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import time
import asyncio

async def download_ready(userid):
    await asyncio.sleep(5)
    print("JOPA!", userid)
    await get_channel_layer().group_send(
        userid,
        {
            'type': 'chat_message',
            'message': 'message'
        }
    )


class ExportConsumer(AsyncJsonWebsocketConsumer):
    async def group_add(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def group_discard(self):
        await  self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def connect(self):
        await self.accept();
        self.user_id = self.room_group_name = self.scope['url_route']['kwargs'].get('user_id')
        print("GROUP NAME", self.room_group_name)
        await self.group_add()

    async def disconnect(self, close_code):
        await self.group_discard()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        request = text_data_json.get('request')
        print('message received!!!', request)
        # await download_ready(self.room_group_name)
        asyncio.create_task(download_ready(self.user_id))
        await self.send_json(content='hello')

    async def chat_message(self, event):
        print("PIZDA!!!!")
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
