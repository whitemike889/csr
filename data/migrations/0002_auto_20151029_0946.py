# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import data.models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='timestamp',
            field=models.DateTimeField(default=data.models.get_now),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='description',
            field=models.CharField(max_length=512, blank=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='classification',
            field=models.CharField(max_length=2, choices=[(b'S', b'Side/App'), (b'B', b'Beverage'), (b'E', b'Entree')]),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=512, verbose_name=b'Item Name', blank=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.CharField(max_length=256, verbose_name=b'Price', blank=True),
        ),
    ]
