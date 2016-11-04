# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-18 01:37
from __future__ import unicode_literals

from django.db import migrations
from datetime import timedelta


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Arduino = apps.get_model("arduino", "Arduino")
    SensorData = apps.get_model("arduino", "SensorData")
    db_alias = schema_editor.connection.alias

    arduinos = Arduino.objects.using(db_alias).all()
    for arduino in arduinos:
        sensors = arduino.arduino_sensors.all()
        if sensors:
            esensor = sensors.filter(data_key='field1')
            if esensor:
                delta = timedelta(seconds=3)
                for edata in esensor[0].sensor_data.all():
                    edatetime = edata.created_at
                    try:
                        epoch = int(edata.data) + 18000
                    except Exception as e:
                        epoch = 0
                    SensorData.objects.filter(
                        arduino_sensor__in=sensors,
                        created_at__gt=edatetime - delta,
                        created_at__lt=edatetime + delta
                    ).update(epoch=epoch)


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('arduino', '0002_sensordata_epoch'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]