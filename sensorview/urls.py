from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sensors.urls')), # Point root to sensors for now
    # path('core/', include('core.urls')), # Uncomment if core app is used
]
