# your_app_name/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import NetworkDevice

@receiver(post_save, sender=NetworkDevice)
def trigger_hardware_alert(sender, instance, **kwargs):
    if instance.update_required:
        channel_layer = get_channel_layer()

        firmware = getattr(instance, 'firmware_version', 'Latest OS Patch')
        alert_html = render_to_string('partials/dashboard_alerts_websocket.html', {
            'device_name': instance.name,
            'firmware': firmware
        })
        
        async_to_sync(channel_layer.group_send)(
            "dashboard_alerts",
            {
                "type": "send_alert",
                "html": alert_html
            }
        )