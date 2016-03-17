# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='KalukulatorWynikowPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=50, verbose_name=b'Nazwa')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='WynikiZawodowPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=50, verbose_name=b'Nazwa')),
                ('events_number', models.IntegerField(default=4, verbose_name=b'Liczba wy\xc5\x9bwietlanych zawod\xc3\xb3w')),
                ('add_preferable', models.BooleanField(default=False, verbose_name=b'Czy wy\xc5\x9bwietli\xc4\x87 w pierwszej kolejno\xc5\x9bci wa\xc5\xbcne pzwla_events')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ZawodyPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=30, verbose_name=b'Nazwa')),
                ('events_number', models.IntegerField(default=4, verbose_name=b'Liczba wy\xc5\x9bwietlanych zawod\xc3\xb3w')),
                ('add_preferable', models.BooleanField(default=True, verbose_name=b'Czy wy\xc5\x9bwietla\xc4\x87 preferowane')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
