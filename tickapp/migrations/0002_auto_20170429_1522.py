# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-29 13:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickapp', 'robo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='show',
            name='video',
        ),
    ]
