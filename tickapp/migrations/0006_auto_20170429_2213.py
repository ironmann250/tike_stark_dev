# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-29 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickapp', '0005_auto_20170429_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='idticket',
        ),
        migrations.AddField(
            model_name='ticket',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
