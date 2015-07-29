# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_instagramdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_id',
            field=models.CharField(default=None, max_length=64, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.CharField(default=None, max_length=64, unique=True),
            preserve_default=False,
        ),
    ]
