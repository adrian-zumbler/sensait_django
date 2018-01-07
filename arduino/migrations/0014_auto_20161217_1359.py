# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-17 19:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arduino', '0013_auto_20161217_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorequipment',
            name='equipment_capacity',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Capacidad'),
        ),
        migrations.AddField(
            model_name='sensorequipment',
            name='equipment_exclusas',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Exclusas'),
        ),
        migrations.AddField(
            model_name='sensorequipment',
            name='equipment_operativerange',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Rango Operativo'),
        ),
        migrations.AlterField(
            model_name='sensorequipment',
            name='equipment_brand',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='sensorequipment',
            name='equipment_comments',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sitio web del Equipo'),
        ),
        migrations.AlterField(
            model_name='sensorequipment',
            name='equipment_model',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Modelo'),
        ),
        migrations.AlterField(
            model_name='sensorequipment',
            name='equipment_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre Equipo'),
        ),
        migrations.AlterField(
            model_name='sensorequipment',
            name='equipment_serial',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='N\xfamero de Serie'),
        ),
        migrations.AlterField(
            model_name='sensorequipment',
            name='equipment_size',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Dimensiones Fisicas'),
        ),
        migrations.AlterField(
            model_name='sensorequipment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', related_query_name='equipments', to='client.Project', verbose_name='Projecto Relacionado'),
        ),
    ]
