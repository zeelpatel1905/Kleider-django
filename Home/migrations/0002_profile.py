# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-18 09:42
from __future__ import unicode_literals

import Home.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('tel', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Enter valid phone number. Phone number must be enterd in the formate : '+9999999999'.", regex='^\\+?1?\\d{9,15}$')])),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'other')], max_length=1)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to=Home.models.upload_image_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]