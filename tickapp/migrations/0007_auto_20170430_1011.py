# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-30 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickapp', '0006_auto_20170429_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='id',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='pin',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]