# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-06 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('poster', models.ImageField(upload_to='media/img')),
                ('video', models.FileField(upload_to='media/video')),
                ('Description', models.CharField(max_length=1000)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField()),
                ('ticket_number', models.IntegerField()),
                ('pin', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(max_length=6)),
                ('password', models.CharField(max_length=40)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickapp.Show')),
            ],
        ),
        migrations.CreateModel(
            name='ticket_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('tike_type', models.CharField(max_length=30)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickapp.Show')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('username', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=40)),
                ('event', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='tickapp.Show')),
            ],
        ),
    ]
