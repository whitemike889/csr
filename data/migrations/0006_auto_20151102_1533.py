# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import data.models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20151029_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuentry',
            name='timefinished',
            field=models.DateTimeField(null=True, blank=True),
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
