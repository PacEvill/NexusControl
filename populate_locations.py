import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorview.settings')
django.setup()

from sensors.models import Sensor, Location, Region

def populate_locations():
    print("Populating regions and locations...")
    
    # Define Regions and their Locations
    structure = {
        'Bloco A': ['Laboratório Principal', 'Sala de Servidores'],
        'Bloco B': ['Estufa 01', 'Estufa 02'],
        'Campus': ['Área Externa Norte', 'Estacionamento'],
        'Administração': ['Sala de Reuniões']
    }
    
    created_locations = []
    
    for region_name, loc_names in structure.items():
        region, _ = Region.objects.get_or_create(name=region_name)
        print(f"Region '{region.name}' created/found.")
        
        for loc_name in loc_names:
            loc, created = Location.objects.get_or_create(
                name=loc_name,
                defaults={'region': region}
            )
            created_locations.append(loc)
            print(f"  Location '{loc.name}' linked to '{region.name}'.")
    
    # Assign sensors to locations
    sensors = Sensor.objects.all()
    if sensors.exists():
        import random
        for sensor in sensors:
            if not sensor.location:
                loc = random.choice(created_locations)
                sensor.location = loc
                sensor.save()
                print(f"Assigned {sensor.name} to {loc.name}")
    else:
        print("No sensors found to assign. Run populate_data.py first or after.")

    print("Done!")

if __name__ == '__main__':
    populate_locations()
