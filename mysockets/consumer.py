from channels.generic.websocket import AsyncWebsocketConsumer
import json, urllib.parse
from db.user import UserDataAccess
from asgiref.sync import async_to_sync

class DataAccessor(AsyncWebsocketConsumer):
    
    async def end_group(self, group_name):
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def connect(self):
        await self.accept()
        
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
        if _type == 'connect':
             if not token:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'data': 'Invalid Token Provided!'
                }))
                self.close()
                return
             await self.channel_layer.group_add(
                f"dataaccess-{token}",
                self.channel_name
            )
             await self.channel_layer.group_send(f"dataaccess-{token}",{
                'type': 'connect.response',
                'status': 'success'})
        if _type == 'send':
            await self.channel_layer.group_send(
                f"dataaccess-{token}",{
                    'type': 'send.data',
                    'data': data.get('data')
                }
            )
            await self.send(text_data=json.dumps({
                'type': 'send_response',
                'status': 'success'}))
    
    async def connect_response(self, event):
        await self.send(text_data=json.dumps({
            'type': 'connect_response',
            'status': event['status']
        }))
    async def send_data(self, event):
        await self.send(text_data=json.dumps({
            'type': 'send',
            'data': event['data']
        }))
            
            
            
            

    async def disconnect(self, close_code):
        pass