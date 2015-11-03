# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import data.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20151103_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktimer',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 3, 15, 56, 37, 924497, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
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
