# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-28 00:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arduino', '0007_auto_20161127_1705'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SensorAlert',
            new_name='ArduinoAlert',
        ),
    ]
