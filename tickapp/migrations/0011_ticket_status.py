# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-13 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickapp', '0010_auto_20170301_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]