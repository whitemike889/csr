# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import data.models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_auto_20151105_1540'),
    ]

    operations = [
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
