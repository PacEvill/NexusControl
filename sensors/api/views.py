from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sensors.models import Sensor, SensorReading
from .serializers import SensorSerializer, SensorReadingSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def reading(self, request, pk=None):
        """
        Endpoint to post a new reading for a specific sensor.
        Payload: { "value": <float> }
        """
        sensor = self.get_object()
        value = request.data.get('value')
        
        if value is None:
            return Response({'error': 'Value is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            value = float(value)
        except ValueError:
             return Response({'error': 'Value must be a number'}, status=status.HTTP_400_BAD_REQUEST)

        # Create reading
        SensorReading.objects.create(sensor=sensor, value=value)
        
        # Update sensor current value and status
        sensor.update_value(value)
        
        return Response({
            'status': 'success',
            'sensor_status': sensor.status,
            'current_value': sensor.value
        })
