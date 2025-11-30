from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .api.views import SensorViewSet

app_name = 'sensors'

router = DefaultRouter()
router.register(r'sensors', SensorViewSet)

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('region/', views.region_dashboard_view, name='region_dashboard'),
    path('list/', views.sensor_list_view, name='sensor_list'),
    path('detail/<int:sensor_id>/', views.sensor_detail_view, name='sensor_detail'),
    path('import/', views.import_data_view, name='import_data'),
    path('export/', views.export_data_view, name='export_data'),
    
    # API
    path('api/v1/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
