# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-03 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20161113_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='nombre_encargado',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Nombre Responsable'),
        ),
    ]
