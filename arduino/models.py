# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from client.models import Client, Project as ProjectC
import uuid


def sensortype_files_name(instance, filename):
    today = timezone.now()
    today_path = today.strftime('%Y/%m/%d')
    return '/'.join(['sensor_type',
                     today_path,
                     'sensor_' + instance.name + '_' + str(instance.id),
                     filename])


class SensorType(models.Model):

    BOOLEAN = 0
    DECIMAL = 1
    INTEGER = 2
    STRING = 3

    DATA_TYPE_CHOICES = (
        (BOOLEAN, 'Booleano'),
        (DECIMAL, 'Decimal'),
        (INTEGER, 'Entero'),
        (STRING, 'Texto')
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=255,
        default=''
    )
    prefix = models.CharField(
        verbose_name='Prefijo',
        max_length=2,
        unique=True,
        default=''
    )
    description = models.CharField(
        verbose_name='Descripción',
        max_length=255,
        default=''
    )
    model = models.CharField(
        verbose_name='Modelo de sensor',
        max_length=255,
        default=''
    )
    data_type = models.PositiveSmallIntegerField(
        choices=DATA_TYPE_CHOICES, default=1)
    data_sheet = models.FileField(
        verbose_name='Ficha técnica',
        upload_to=sensortype_files_name,
        blank=True,
        null=True
    )
    data_image = models.FileField(
        verbose_name='Imagen del sensor',
        upload_to=sensortype_files_name,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name + ': ' + self.description


class Arduino(models.Model):

    ESTATUS_CHOICES = (
        (1, 'Diseño'),
        (2, 'Construcción'),
        (3, 'Implementación'),
        (4, 'Mantenimiento/Pruebas'),
        (5, 'Producción'),
        (6, 'Fallo de Sistema')
    )

    project = models.ForeignKey(ProjectC, related_name="arduinos")
    name = models.CharField(max_length=255)
    arduino_token = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    sensors = models.ManyToManyField(SensorType, through='ArduinoSensor')
    available_sensors = models.SmallIntegerField(default=1)
    estatus = models.PositiveSmallIntegerField(verbose_name='Estatus', choices=ESTATUS_CHOICES, default=1)

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
    max_value = models.DecimalField(
        verbose_name='Valor máximo permitido',
        max_digits=8,
        decimal_places=4,
        blank=True,
        null=True
    )
    min_value = models.DecimalField(
        verbose_name='Valor mínimo permitido',
        max_digits=8,
        decimal_places=4,
        blank=True,
        null=True
    )

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
