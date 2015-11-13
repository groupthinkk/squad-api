# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0004_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends_and_family',
            field=models.BooleanField(default=False),
        ),
    ]
