from rest_framework import serializers
from arduino.models import ArduinoSensor, Arduino, Sensor, SensorData


class ArduinoSerializer(serializers.ModelSerializer):

    arduino_token = serializers.CharField(read_only=True)

    class Meta:
        model = Arduino
        fields = '__all__'
        #exclude = ('arduino_token', )


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class ArduinoSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArduinoSensor
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