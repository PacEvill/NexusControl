from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
import csv
import json
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from .models import Sensor, Location, SensorAlert, SensorReading, Region, SensorType

def dashboard_view(request):
    """Main dashboard view"""
    location_id = request.GET.get('location')
    sensors = Sensor.objects.all()
    
    if location_id:
        sensors = sensors.filter(location_id=location_id)
    
    # Statistics
    total_sensors = sensors.count()
    online_sensors = sensors.filter(status='normal').count()
    offline_sensors = sensors.filter(status='disconnected').count()
    error_sensors = sensors.filter(status='error').count()
    
    # Recent Alerts (filtered by location sensors if selected)
    recent_alerts = SensorAlert.objects.filter(is_resolved=False)
    if location_id:
        recent_alerts = recent_alerts.filter(sensor__location_id=location_id)
    recent_alerts = recent_alerts.order_by('-timestamp')[:5]
    
    # Locations for filter dropdown
    locations = Location.objects.all()
    
    # Quick Stats (Mocked for now, can be real later)
    avg_temp = 23.5 # Placeholder
    
    context = {
        'sensors': sensors,
        'stats': {
            'total': total_sensors,
            'online': online_sensors,
            'offline': offline_sensors,
            'error': error_sensors,
        },
        'recent_alerts': recent_alerts,
        'locations': locations,
        'selected_location': int(location_id) if location_id else None,
        'page_title': 'Dashboard'
    }
    return render(request, 'sensors/dashboard.html', context)

def region_dashboard_view(request):
    """Command Center view aggregated by Region"""
    regions = Region.objects.prefetch_related('locations__sensors').all()
    
    region_stats = []
    for region in regions:
        sensors = Sensor.objects.filter(location__region=region)
        stats = {
            'region': region,
            'total': sensors.count(),
            'online': sensors.filter(status='normal').count(),
            'alerts': sensors.filter(status__in=['warning', 'alert']).count(),
            'locations_count': region.locations.count()
        }
        region_stats.append(stats)
    
    context = {
        'region_stats': region_stats,
        'page_title': 'Command Center'
    }
    return render(request, 'sensors/region_dashboard.html', context)

def export_data_view(request):
    """Export sensor data to CSV or JSON"""
    format_type = request.GET.get('format', 'csv')
    sensors = Sensor.objects.all()
    
    if format_type == 'json':
        data = list(sensors.values(
            'id', 'name', 'location__name', 'sensor_type__name', 
            'value', 'unit', 'status', 'last_update'
        ))
        return JsonResponse(data, safe=False, encoder=DjangoJSONEncoder)
    
    # Default to CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sensors_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Location', 'Type', 'Value', 'Unit', 'Status', 'Last Update'])
    
    for s in sensors:
        writer.writerow([
            s.id, s.name, s.location.name if s.location else '', 
            s.sensor_type.name if s.sensor_type else '', 
            s.value, s.unit, s.status, s.last_update
        ])
        
    return response

from .forms import SensorImportForm
import io

def import_data_view(request):
    """Handle data import from CSV"""
    if request.method == 'POST':
        form = SensorImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Por favor, envie um arquivo CSV.')
                return redirect('sensors:import_data')
            
            try:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string) # Skip header
                
                created_count = 0
                updated_count = 0
                
                for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                    # Expected format: ID, Name, Location, Type, Value, Unit, Status, Last Update
                    # We will try to match by Name or ID if provided, otherwise create new
                    
                    # Basic validation
                    if len(column) < 4:
                        continue
                        
                    sensor_name = column[1]
                    location_name = column[2]
                    type_name = column[3]
                    try:
                        value = float(column[4])
                    except:
                        value = 0.0
                    
                    # Get or Create related objects
                    location = None
                    if location_name:
                        location, _ = Location.objects.get_or_create(name=location_name)
                        
                    sensor_type = None
                    if type_name:
                        # Simple lookup, might need more robust logic if types have codes
                        sensor_type, _ = SensorType.objects.get_or_create(
                            name=type_name, 
                            defaults={'code': type_name.lower().replace(' ', '_'), 'unit': column[5] or ''}
                        )
                    
                    # Update or Create Sensor
                    sensor, created = Sensor.objects.update_or_create(
                        name=sensor_name,
                        defaults={
                            'location': location,
                            'sensor_type': sensor_type,
                            'value': value,
                            'unit': column[5],
                            'status': column[6] if len(column) > 6 else 'normal'
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                messages.success(request, f"Importação concluída: {created_count} criados, {updated_count} atualizados.")
                return redirect('sensors:dashboard')
                
            except Exception as e:
                messages.error(request, f"Erro ao processar arquivo: {e}")
                return redirect('sensors:import_data')
    else:
        form = SensorImportForm()
        
    return render(request, 'sensors/import_data.html', {'form': form, 'page_title': 'Importar Dados'})

def sensor_list_view(request):
    """List all sensors"""
    sensors = Sensor.objects.all()
    context = {
        'sensors': sensors,
        'page_title': 'Sensores'
    }
    return render(request, 'sensors/sensor_list.html', context)

def sensor_detail_view(request, sensor_id):
    """Detail view for a specific sensor"""
    sensor = get_object_or_404(Sensor, id=sensor_id)
    readings = sensor.readings.all()[:50] # Last 50 readings
    alerts = sensor.alerts.all()[:10]
    
    context = {
        'sensor': sensor,
        'readings': readings,
        'alerts': alerts,
        'page_title': sensor.name
    }
    return render(request, 'sensors/sensor_detail.html', context)
