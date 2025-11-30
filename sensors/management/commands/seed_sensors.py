from django.core.management.base import BaseCommand
from sensors.models import Sensor


class Command(BaseCommand):
    help = 'Seed the database with sample sensors'

    def handle(self, *args, **options):
        Sensor.objects.all().delete()
        for i in range(1, 7):
            Sensor.objects.create(
                id=f'sensor_{i}',
                name=f'Sensor {i}',
                type='temperature',
                connection_type='wifi',
                status='connected' if i % 2 == 0 else 'available',
            )
        self.stdout.write(self.style.SUCCESS('Seeded sensors'))
