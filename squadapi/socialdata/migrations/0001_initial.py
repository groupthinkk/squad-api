# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.TextField()),
                ('likes_count', models.IntegerField()),
                ('comments_count', models.IntegerField()),
                ('created_datetime', models.DateTimeField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstagramUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='instagrampost',
            name='user',
            field=models.ForeignKey(to='socialdata.InstagramUser'),
        ),
    ]
