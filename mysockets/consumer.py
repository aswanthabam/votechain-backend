from channels.generic.websocket import AsyncWebsocketConsumer
import json, urllib.parse
from db.user import UserDataAccess
from asgiref.sync import async_to_sync

class DataAccessor(AsyncWebsocketConsumer):
    
    async def end_group(self, group_name):
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def connect(self):
        await self.accept()
        query = urllib.parse.parse_qs(self.scope["query_string"].decode('utf-8'))
        token = query.get('token')
        if not token:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'data': 'Invalid Token Provided!'
            }))
            self.close()
            return
        token = token[0]
        await self.channel_layer.group_add(
            f"dataaccess-{token}",
            self.channel_name
        )
        
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        _type = data.get('type')
        token = data.get("token")
        if not _type or not token:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'data': 'Invalid Data Provided!'
            }))
            return
        if _type == 'send':
            await self.channel_layer.group_send(
                f"dataaccess-{token}",{
                    'type': 'send.data',
                    'data': data.get('data')
                }
            )

    async def send_data(self, event):
        await self.send(text_data=json.dumps({
            'type': 'send',
            'data': event['data']
        }))
            
            
            
            

    def disconnect(self, close_code):
        pass