# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-10-12 01:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knit_process',
            name='knit_machine_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='knit_machine_code', to='machine.Knit_Machine'),
        ),
    ]
