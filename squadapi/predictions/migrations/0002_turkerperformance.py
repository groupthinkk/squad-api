# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TurkerPerformance',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('correctness', models.FloatField(db_index=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('turker', models.OneToOneField(to='predictions.Turker')),
            ],
        ),
    ]
