# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import data.models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20151029_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='timestamp',
            field=models.DateTimeField(default=data.models.get_now),
        ),
    ]
