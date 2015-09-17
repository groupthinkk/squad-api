# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0003_auto_20150731_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
