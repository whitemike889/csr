# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import data.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0006_auto_20151102_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkTimer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('token', models.CharField(max_length=256)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
