# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-12 00:16
from __future__ import unicode_literals

import arduino.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0004_auto_20160825_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arduino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('arduino_token', models.CharField(max_length=20, unique=True)),
                ('location', models.CharField(max_length=255)),
                ('available_sensors', models.SmallIntegerField(default=1)),
                ('estatus', models.PositiveSmallIntegerField(choices=[(1, 'Dise\xf1o'), (2, 'Construcci\xf3n'), (3, 'Implementaci\xf3n'), (4, 'Mantenimiento/Pruebas'), (5, 'Producci\xf3n'), (6, 'Fallo de Sistema')], default=1, verbose_name='Estatus')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arduinos', to='client.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ArduinoSensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('index', models.PositiveSmallIntegerField()),
                ('data_key', models.CharField(max_length=20)),
                ('max_value', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True, verbose_name='Valor m\xe1ximo permitido')),
                ('min_value', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True, verbose_name='Valor m\xednimo permitido')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('arduino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arduino_sensors', to='arduino.Arduino')),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('arduino_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_data', related_query_name='sensor_data', to='arduino.ArduinoSensor')),
            ],
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, verbose_name='Nombre')),
                ('prefix', models.CharField(default='', max_length=2, unique=True, verbose_name='Prefijo')),
                ('description', models.CharField(default='', max_length=255, verbose_name='Descripci\xf3n')),
                ('model', models.CharField(default='', max_length=255, verbose_name='Modelo de sensor')),
                ('data_type', models.PositiveSmallIntegerField(choices=[(0, 'Booleano'), (1, 'Decimal'), (2, 'Entero'), (3, 'Texto')], default=1)),
                ('data_sheet', models.FileField(blank=True, null=True, upload_to=arduino.models.sensortype_files_name, verbose_name='Ficha t\xe9cnica')),
                ('data_image', models.FileField(blank=True, null=True, upload_to=arduino.models.sensortype_files_name, verbose_name='Imagen del sensor')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='arduinosensor',
            name='sensor_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arduino.SensorType'),
        ),
        migrations.AddField(
            model_name='arduino',
            name='sensors',
            field=models.ManyToManyField(through='arduino.ArduinoSensor', to='arduino.SensorType'),
        ),
    ]
