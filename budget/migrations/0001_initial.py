# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now=True)),
                ('essential', models.BooleanField(default=False)),
                ('is_expense', models.BooleanField(default=True)),
                ('category', models.ForeignKey(to='budget.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
