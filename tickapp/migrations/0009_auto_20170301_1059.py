# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-01 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickapp', '0008_ticket_ticket_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='phone_number',
            field=models.IntegerField(null=True),
        ),
    ]
