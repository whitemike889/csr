# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import data.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=512)),
                ('timestamp', models.DateTimeField(default=data.models.get_now)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=512, verbose_name=b'Filename')),
            ],
        ),
        migrations.CreateModel(
            name='MenuEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('restaurantName', models.CharField(max_length=512, verbose_name=b'Restaurant Name')),
                ('finished', models.IntegerField(default=0, choices=[(0, b'No'), (1, b'Yes')])),
                ('menu', models.ForeignKey(to='data.Menu')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, verbose_name=b'Item Name')),
                ('price', models.CharField(max_length=256, verbose_name=b'Price')),
                ('classification', models.CharField(default=None, max_length=2, choices=[(b'S', b'Side/App'), (b'B', b'Beverage'), (b'E', b'Entree')])),
                ('menuentry', models.ForeignKey(to='data.MenuEntry')),
            ],
        ),
        migrations.AddField(
            model_name='eventlog',
            name='menuentry',
            field=models.ForeignKey(to='data.MenuEntry'),
        ),
    ]
