from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from client.models import Client, Project as ProjectC
import uuid


# class ArduinoManager(models.Manager):
#    def create(self):
#        pass


# TODO: Eliminar este modelo
# class Project(models.Model):
#     user = models.ForeignKey(User)
#     client = models.ForeignKey(Client, related_name='projectos', blank=True, null=True)
#     name = models.CharField(max_length=255)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __unicode__(self):
#         return self.name


class SensorType(models.Model):
    name = models.CharField(max_length=255)
    prefix = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name + ': ' + self.description


class Arduino(models.Model):
    project = models.ForeignKey(ProjectC, related_name="arduinos")
    name = models.CharField(max_length=255)
    arduino_token = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    sensors = models.ManyToManyField(SensorType, through='ArduinoSensor')
    available_sensors = models.SmallIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = ArduinoManager()

    def __unicode__(self):
        return 'ID Arduino: ' + self.arduino_token

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.arduino_token = str(uuid.uuid4().hex)
        # self.objects.filter(arduino_id=self.arduino_id)
        super(Arduino, self).save(force_insert, force_update, using, update_fields)


class ArduinoSensor(models.Model):
    arduino = models.ForeignKey(
        Arduino,
        # related_name='arduino_sensors',
        # to_field='arduino_token',
        on_delete=models.CASCADE
    )
    sensor_type = models.ForeignKey(
        SensorType,
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255)
    index = models.PositiveSmallIntegerField()
    data_key = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)
        #return 'Arduino: {0}, Sensor: {1} ({2})'.format(
        #    self.arduino.arduino_token,
        #    self.sensor_type.prefix,
        #    self.description
        #)


class SensorData(models.Model):
    arduino_sensor = models.ForeignKey(
        ArduinoSensor,
        related_name='sensor_data',
        related_query_name='sensor_data',
        on_delete=models.CASCADE,
    )
    data = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
