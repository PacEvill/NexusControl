from django.test import TestCase, Client
from django.urls import reverse
from sensors.models import Sensor, SensorType, Location, Region, SensorReading

class SensorModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Test Region")
        self.location = Location.objects.create(name="Test Location", region=self.region)
        self.sensor_type = SensorType.objects.create(
            name="Test Type", 
            code="test_type", 
            unit="T",
            min_value_default=0,
            max_value_default=100
        )
        self.sensor = Sensor.objects.create(
            name="Test Sensor",
            location=self.location,
            sensor_type=self.sensor_type,
            value=50.5
        )

    def test_sensor_creation(self):
        """Test if sensor is created correctly"""
        self.assertEqual(self.sensor.name, "Test Sensor")
        self.assertEqual(self.sensor.location.name, "Test Location")
        self.assertEqual(self.sensor.sensor_type.name, "Test Type")
        self.assertEqual(self.sensor.unit, "T") # Should inherit from type

    def test_sensor_str(self):
        """Test string representation"""
        self.assertEqual(str(self.sensor), "Test Sensor (50.5 T)")

class SensorLogicTest(TestCase):
    def setUp(self):
        self.sensor = Sensor.objects.create(
            name="Logic Sensor",
            min_value=10,
            max_value=90,
            warning_min=20,
            warning_max=80,
            value=50,
            status='normal'
        )

    def test_update_value_normal(self):
        self.sensor.update_value(50)
        self.assertEqual(self.sensor.status, 'normal')

    def test_update_value_warning_high(self):
        self.sensor.update_value(85)
        self.assertEqual(self.sensor.status, 'warning')

    def test_update_value_warning_low(self):
        self.sensor.update_value(15)
        self.assertEqual(self.sensor.status, 'warning')

    def test_update_value_alert_high(self):
        self.sensor.update_value(95)
        self.assertEqual(self.sensor.status, 'alert')

    def test_update_value_alert_low(self):
        self.sensor.update_value(5)
        self.assertEqual(self.sensor.status, 'alert')

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('sensors:dashboard') # Assuming 'sensors' namespace

    def test_dashboard_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_context(self):
        response = self.client.get(self.url)
        self.assertIn('stats', response.context)
        self.assertIn('sensors', response.context)
