from django.conf.urls import url, include
from rest_framework_nested import routers

from arduino.views import (ArduinoViewSet, SensorViewSet, DataViewSet,
                           ArduinoSensorViewSet, SensorDataViewSet)

router = routers.DefaultRouter()
router.register(r'arduinos', ArduinoViewSet, base_name='device')
router.register(r'sensors', SensorViewSet, base_name='sensor')
router.register(r'data', DataViewSet, base_name='data')

arduino_router = routers.NestedSimpleRouter(router, r'arduinos', lookup='arduino')
arduino_router.register(r'sensors', ArduinoSensorViewSet, base_name='device-sensor')

sensor_data_router = routers.NestedSimpleRouter(arduino_router, r'sensors', lookup='sensor')
sensor_data_router.register('data', SensorDataViewSet, base_name='device-sensor-data')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(arduino_router.urls)),
    url(r'^api/', include(sensor_data_router.urls)),
]
