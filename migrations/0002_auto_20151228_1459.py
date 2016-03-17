# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zawody_plugin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zawodyplugin',
            name='add_preferable',
            field=models.BooleanField(default=True, verbose_name=b'Czy wy\xc5\x9bwietla\xc4\x87 preferowane'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='zawodyplugin',
            name='events_number',
            field=models.IntegerField(default=4, verbose_name=b'Liczba wy\xc5\x9bwietlanych zawod\xc3\xb3w'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zawodyplugin',
            name='name',
            field=models.CharField(max_length=30, verbose_name=b'Nazwa'),
            preserve_default=True,
        ),
    ]
