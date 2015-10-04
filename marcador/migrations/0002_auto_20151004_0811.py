# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marcador', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookmark',
            options={'ordering': ['date_created'], 'verbose_name_plural': 'bookmarks', 'verbose_name': 'bookmark'},
        ),
    ]
