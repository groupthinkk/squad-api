# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Normalization',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to='instagram.User')),
                ('data', models.TextField()),
            ],
        ),
    ]
