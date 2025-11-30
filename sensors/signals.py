from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Sensor, SensorReading

@receiver(post_save, sender=SensorReading)
def broadcast_sensor_update(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        sensor = instance.sensor
        
        data = {
            'sensor_id': sensor.id,
            'sensor_name': sensor.name,
            'value': instance.value,
            'unit': sensor.unit,
            'status': sensor.status,
            'timestamp': instance.timestamp.isoformat()
        }
        
        async_to_sync(channel_layer.group_send)(
            'dashboard_group',
            {
                'type': 'sensor_update',
                'message': data
            }
        )
