# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-03 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arduino', '0011_auto_20161203_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='arduino',
            name='delta_time_alerts',
            field=models.PositiveSmallIntegerField(default=5, verbose_name='Tiempo entre envio de alertas'),
        ),
    ]