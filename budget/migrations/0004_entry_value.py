# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_auto_20160403_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]
