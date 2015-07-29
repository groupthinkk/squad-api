# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('post_id', models.CharField(max_length=64, unique=True)),
                ('caption', models.TextField()),
                ('image_url', models.URLField()),
                ('likes_count', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('created_datetime', models.DateTimeField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('user_id', models.CharField(max_length=64, default='', blank=True)),
                ('username', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Normalization',
            fields=[
                ('user', models.OneToOneField(serialize=False, to='instagram.User', primary_key=True)),
                ('data', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to='instagram.User'),
        ),
    ]
