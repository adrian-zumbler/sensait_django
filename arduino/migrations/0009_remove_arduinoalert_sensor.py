# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-28 00:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arduino', '0008_auto_20161127_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arduinoalert',
            name='sensor',
        ),
    ]