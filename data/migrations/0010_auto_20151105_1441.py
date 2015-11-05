# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import data.models
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('data', '0009_auto_20151103_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='menuentry',
            name='timestarted',
            field=models.DateTimeField(default=data.models.get_now),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='timestarted',
            field=models.DateTimeField(default=data.models.get_now),
        ),
    ]
