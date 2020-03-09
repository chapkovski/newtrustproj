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
import random
from trust.models import Player
from channels.db import database_sync_to_async


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
    groups = ['jopa']

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
        print(self.groups, 'GROUPS')

    async def disconnect(self, close_code):
        await self.group_discard()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        request = text_data_json.get('request')
        print('message received!!!', request)
        # await download_ready(self.room_group_name)
        asyncio.create_task(self.delayed_task())
        await self.send_json(content='hello')

    @database_sync_to_async
    def get_long_q(self):

        maxp = Player.objects.all().count() - 1
        ps = []
        print('IN THE BGINING OF DEALY')
        if maxp > 0:
            for i in Player.objects.all():
                ps.append(random.choice(Player.objects.all()).participant.code)
        return random.choice(ps)

    async def delayed_task(self):
        q = await self.get_long_q()
        print('DB', q)
        await self.send_json({'a': q})

    async def delayed_message(self, event):
        asyncio.create_task(self.delayed_task())
        await self.send_json('NOW')

    async def chat_message(self, event):
        message = event['message']
        await self.send_json(message)
