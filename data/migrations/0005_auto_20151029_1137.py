# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import data.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20151029_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='timestamp',
            new_name='timefinshed',
        ),
        migrations.AddField(
            model_name='menuentry',
            name='timefinished',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 29, 16, 37, 16, 943298, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menuentry',
            name='timestarted',
            field=models.DateTimeField(default=data.models.get_now),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='timestarted',
            field=models.DateTimeField(default=data.models.get_now),
        ),
    ]
