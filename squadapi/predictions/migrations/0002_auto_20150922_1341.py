# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramprediction',
            name='correct',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instagramprediction',
            name='ux_id',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='turker',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 40, 56, 88424, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='turker',
            name='updated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 41, 10, 354631, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
