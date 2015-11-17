# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0003_instagrampost'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagrampost',
            name='updated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 17, 6, 21, 54, 373887, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
