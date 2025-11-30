import os
import django
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorview.settings')
django.setup()

from sensors.models import Sensor, SensorAlert, SensorReading, SensorType

def populate():
    print("Populating data...")
    
    # Create Sensor Types
    types_data = [
        {'name': 'Temperatura', 'code': 'temperature', 'unit': '°C', 'icon': 'bi-thermometer-half', 'min': 18, 'max': 28},
        {'name': 'Umidade', 'code': 'humidity', 'unit': '%', 'icon': 'bi-droplet-half', 'min': 30, 'max': 70},
        {'name': 'Pressão', 'code': 'pressure', 'unit': 'hPa', 'icon': 'bi-speedometer', 'min': 900, 'max': 1100},
        {'name': 'Movimento', 'code': 'motion', 'unit': '', 'icon': 'bi-person-walking', 'min': 0, 'max': 1},
        {'name': 'Luz', 'code': 'light', 'unit': 'lux', 'icon': 'bi-sun', 'min': 0, 'max': 10000},
    ]
    
    created_types = {}
    for t_data in types_data:
        st, created = SensorType.objects.get_or_create(
            code=t_data['code'],
            defaults={
                'name': t_data['name'],
                'unit': t_data['unit'],
                'icon': t_data['icon'],
                'min_value_default': t_data['min'],
                'max_value_default': t_data['max']
            }
        )
        created_types[t_data['code']] = st
        print(f"SensorType {st.name} created/found.")

    # Create Sensors
    sensors_data = [
        {'name': 'Sensor Temp Lab', 'type_code': 'temperature'},
        {'name': 'Sensor Umid Lab', 'type_code': 'humidity'},
        {'name': 'Sensor Pressão', 'type_code': 'pressure'},
        {'name': 'Sensor Movimento Hall', 'type_code': 'motion'},
        {'name': 'Sensor Luz Ext', 'type_code': 'light'},
    ]
    
    created_sensors = []
    for data in sensors_data:
        st = created_types[data['type_code']]
        sensor, created = Sensor.objects.get_or_create(
            name=data['name'],
            defaults={
                'sensor_type': st,
                'unit': st.unit,
                'min_value': st.min_value_default,
                'max_value': st.max_value_default,
                'value': random.uniform(st.min_value_default, st.max_value_default),
                'status': 'normal'
            }
        )
        created_sensors.append(sensor)
        print(f"Sensor {sensor.name} created/updated.")

    # Create Readings
    for sensor in created_sensors:
        for i in range(10):
            SensorReading.objects.create(
                sensor=sensor,
                value=random.uniform(sensor.min_value, sensor.max_value),
                timestamp=timezone.now() - timezone.timedelta(minutes=i*10)
            )
    
    # Create Alerts
    if created_sensors:
        SensorAlert.objects.create(
            sensor=created_sensors[0],
            message="Temperatura acima do normal",
            severity="warning",
            timestamp=timezone.now() - timezone.timedelta(minutes=5)
        )
        SensorAlert.objects.create(
            sensor=created_sensors[1],
            message="Umidade crítica",
            severity="critical",
            timestamp=timezone.now() - timezone.timedelta(minutes=30)
        )

    print("Done!")

if __name__ == '__main__':
    populate()
