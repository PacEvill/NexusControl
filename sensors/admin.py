from django.contrib import admin
from .models import Sensor, Location, SensorLog, SensorAlert, Region, SensorType

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'created_at')
    search_fields = ('name', 'manager')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'created_at')
    search_fields = ('name', 'region__name')
    list_filter = ('region',)

@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'unit', 'icon')
    search_fields = ('name', 'code')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'sensor_type', 'connection_type', 'status', 'value', 'unit', 'last_update')
    search_fields = ('id', 'name', 'location__name')
    list_filter = ('location', 'status', 'sensor_type', 'connection_type')

@admin.register(SensorLog)
class SensorLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action')
    list_filter = ('action', 'timestamp')

@admin.register(SensorAlert)
class SensorAlertAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'sensor', 'severity', 'message', 'is_resolved')
    list_filter = ('severity', 'is_resolved')
