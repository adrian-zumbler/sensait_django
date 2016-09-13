from rest_framework import serializers
from arduino.models import ArduinoSensor, Arduino, SensorType, SensorData


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = '__all__'


class ArduinoSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArduinoSensor
        fields = '__all__'


class ArduinoSerializer(serializers.ModelSerializer):

    arduino_token = serializers.CharField(read_only=True)
    sensors = ArduinoSensorSerializer(source='arduino_sensors', many=True)

    class Meta:
        model = Arduino
        fields = '__all__'


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

    def save(self, **kwargs):
        return super(SensorDataSerializer, self).save(**kwargs)


class ArduinoDataSerializer(serializers.Serializer):
    arduino = ArduinoSerializer()
    data = serializers.CharField()
