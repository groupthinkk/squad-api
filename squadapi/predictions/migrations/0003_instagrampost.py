# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0006_auto_20151113_0345'),
        ('predictions', '0002_turkerperformance'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('hit_id', models.CharField(max_length=128)),
                ('lower_bound', models.IntegerField()),
                ('upper_bound', models.IntegerField()),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(to='instagram.Post')),
            ],
        ),
    ]
