from django.contrib import admin
from arduino.models import Arduino, SensorType, ArduinoSensor



class ArduinoFieldDataInline(admin.TabularInline):
    model = ArduinoSensor
    extra = 3


class ArduinoAdmin(admin.ModelAdmin):
    inlines = (ArduinoFieldDataInline, )


class SensorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Arduino, ArduinoAdmin)
admin.site.register(SensorType)
