# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_auto_20160404_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(),
        ),
    ]