# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-17 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arduino', '0012_arduino_delta_time_alerts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsend',
            name='subject',
            field=models.CharField(max_length=255),
        ),
    ]
