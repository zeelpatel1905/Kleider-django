# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-22 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0006_auto_20181222_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('O', 'other'), ('F', 'Female'), ('M', 'Male')], max_length=1),
        ),
        migrations.AlterModelTable(
            name='help',
            table=None,
        ),
    ]
