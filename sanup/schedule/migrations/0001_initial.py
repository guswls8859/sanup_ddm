# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-06-17 01:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('machine', '0001_initial'),
        ('order', '0001_initial'),
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Knit_Beam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('knit_external', models.IntegerField(null=True)),
                ('knit_current_external', models.IntegerField(null=True)),
                ('knit_turn_cnt', models.IntegerField(null=True)),
                ('knit_current_turn_cnt', models.IntegerField(null=True)),
                ('knit_yarn_thick', models.IntegerField(null=True)),
                ('beam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.Beam')),
            ],
            options={
                'db_table': 'Knit_Beam',
            },
        ),
        migrations.CreateModel(
            name='Knit_Machine_Realtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trs_operation_number', models.IntegerField(null=True)),
                ('trs_total_run_course', models.IntegerField(null=True)),
                ('trs_state', models.IntegerField(null=True)),
                ('trs_stopmark', models.IntegerField(null=True)),
                ('trs_onetime_prdt', models.IntegerField(null=True)),
                ('trs_set_prdt', models.IntegerField(null=True)),
                ('trs_run_course', models.IntegerField(null=True)),
                ('trs_total_oper_time', models.DateTimeField(null=True)),
                ('trs_total_accum_time', models.DateTimeField(null=True)),
                ('trs_meter', models.FloatField(null=True)),
                ('trs_total_meter', models.IntegerField(null=True)),
                ('trs_accumulate_meter', models.IntegerField(null=True)),
                ('trs_key_angle', models.IntegerField(null=True)),
                ('trs_rpm_main', models.IntegerField(null=True)),
                ('trs_sensor_01', models.IntegerField(null=True)),
                ('trs_sensor_02', models.IntegerField(null=True)),
                ('trs_sensor_03', models.IntegerField(null=True)),
                ('trs_sensor_04', models.IntegerField(null=True)),
                ('trs_sensor_05', models.IntegerField(null=True)),
                ('trs_sensor_06', models.IntegerField(null=True)),
                ('trs_sensor_07', models.IntegerField(null=True)),
                ('trs_sensor_08', models.IntegerField(null=True)),
                ('trs_sensor_09', models.IntegerField(null=True)),
                ('trs_sensor_10', models.IntegerField(null=True)),
                ('trs_onoff', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'Knit_Machine_Realtime',
            },
        ),
        migrations.CreateModel(
            name='Knit_Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=None, null=True)),
                ('end_time', models.DateTimeField(default=None, null=True)),
                ('real_start_time', models.DateTimeField(default=None, null=True)),
                ('real_end_time', models.DateTimeField(default=None, null=True)),
                ('knit_machine_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='machine.Knit_Machine')),
                ('order_designdata', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.Order_DesignData')),
                ('yw_knit_machine_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='machine.YW_Knit_Machine')),
            ],
            options={
                'db_table': 'Knit_Process',
            },
        ),
        migrations.CreateModel(
            name='Warp_Beam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external', models.IntegerField(null=True)),
                ('current_external', models.IntegerField(null=True)),
                ('turn_cnt', models.IntegerField(null=True)),
                ('current_turn_cnt', models.IntegerField(null=True)),
                ('yarn_thick', models.IntegerField(null=True)),
                ('yarn_count', models.IntegerField(null=True)),
                ('yarn_meter', models.IntegerField(null=True)),
                ('yarn_current_meter', models.IntegerField(null=True)),
                ('beam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.Beam')),
            ],
            options={
                'db_table': 'Warp_Beam',
            },
        ),
        migrations.CreateModel(
            name='Warp_Machine_Realtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tws_start_date', models.DateTimeField(null=True)),
                ('tws_start_time', models.DateTimeField(null=True)),
                ('tws_meter', models.IntegerField(null=True)),
                ('tws_state', models.IntegerField(null=True)),
                ('tws_hoist_state', models.IntegerField(null=True)),
                ('tws_oiling_state', models.IntegerField(null=True)),
                ('tws_clamp_state', models.IntegerField(null=True)),
                ('tws_w_inverter_state', models.IntegerField(null=True)),
                ('tws_s_inverter_state', models.IntegerField(null=True)),
                ('tws_c_inverter_state', models.IntegerField(null=True)),
                ('tws_current_turncnt', models.IntegerField(null=True)),
                ('tws_runtime', models.DateTimeField(null=True)),
                ('tws_current_meter', models.IntegerField(null=True)),
                ('tws_kia', models.IntegerField(null=True)),
                ('tws_warper_speed', models.FloatField(null=True)),
                ('tws_warper_outside', models.IntegerField(null=True)),
                ('tws_warper_total_length', models.FloatField(null=True)),
                ('tws_creel_total_length', models.IntegerField(null=True)),
                ('tws_creel_speed', models.IntegerField(null=True)),
                ('tws_elongation_rate', models.IntegerField(null=True)),
                ('tws_relax_deviation', models.IntegerField(null=True)),
                ('tws_error', models.DateTimeField(null=True)),
                ('tws_onoff', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'Warp_Machine_Realtime',
            },
        ),
        migrations.CreateModel(
            name='Warp_Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=None, null=True)),
                ('end_time', models.DateTimeField(default=None, null=True)),
                ('real_start_time', models.DateTimeField(default=None, null=True)),
                ('real_end_time', models.DateTimeField(default=None, null=True)),
                ('order_designdata', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.Order_DesignData')),
                ('warp_machine_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='machine.Warp_Machine')),
                ('yw_warp_machine_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='machine.YW_Warp_Machine')),
            ],
            options={
                'db_table': 'Warp_Process',
            },
        ),
        migrations.AddField(
            model_name='warp_machine_realtime',
            name='warp_process',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.Warp_Process'),
        ),
        migrations.AddField(
            model_name='warp_beam',
            name='warp_process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Warp_Process'),
        ),
        migrations.AddField(
            model_name='knit_machine_realtime',
            name='knit_process',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.Knit_Process'),
        ),
        migrations.AddField(
            model_name='knit_beam',
            name='knit_process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Knit_Process'),
        ),
    ]
