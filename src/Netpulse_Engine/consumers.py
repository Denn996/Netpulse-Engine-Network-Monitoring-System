# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "dashboard_alerts"

        # Join the dashboard alerts group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # This handles messages sent from the backend code
    async def send_alert(self, event):
        # Send the HTML snippet directly to the frontend
        await self.send(text_data=json.dumps({
            'html': event['html']
        }))