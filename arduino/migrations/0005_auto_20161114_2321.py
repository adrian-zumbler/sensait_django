# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-15 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arduino', '0004_sensortype_subfix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensortype',
            name='subfix',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Subfijo'),
        ),
    ]