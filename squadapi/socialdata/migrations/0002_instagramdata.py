# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramData',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to='socialdata.InstagramUser')),
                ('data', models.TextField()),
            ],
        ),
    ]
