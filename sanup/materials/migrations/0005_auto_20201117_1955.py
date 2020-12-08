# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-11-17 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_auto_20201117_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='raw',
            name='request_com',
            field=models.CharField(default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='beam',
            name='Receivingdate',
            field=models.CharField(default='2020-11-17 19:55', max_length=30),
        ),
        migrations.AlterField(
            model_name='roll',
            name='receivingdate',
            field=models.DateTimeField(blank=True, default='2020-11-17 19:55', null=True),
        ),
        migrations.AlterField(
            model_name='yarn',
            name='Receivingdate',
            field=models.CharField(default='2020-11-17 19:55', max_length=30),
        ),
    ]
