# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.IntegerField(default=0),
        ),
    ]
