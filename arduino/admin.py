from django.contrib import admin
from arduino.models import Arduino, Sensor, ArduinoSensor, Project


class ArduinoFieldDataInline(admin.TabularInline):
    model = ArduinoSensor
    extra = 3


class ArduinoAdmin(admin.ModelAdmin):
    inlines = (ArduinoFieldDataInline, )


class SensorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project)
admin.site.register(Arduino)
admin.site.register(Sensor)
