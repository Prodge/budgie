# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
