# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_management', '0004_auto_20171115_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleroom',
            name='teacher_group',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacher',
            name='proj_group_exam',
            field=models.IntegerField(default=0),
        ),
    ]