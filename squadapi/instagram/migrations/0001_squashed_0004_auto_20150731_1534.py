# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('instagram', '0001_initial'), ('instagram', '0002_user_followers'), ('instagram', '0003_auto_20150731_1532'), ('instagram', '0004_auto_20150731_1534')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('post_id', models.CharField(unique=True, max_length=64)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('user_id', models.CharField(blank=True, default='', max_length=64)),
                ('username', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Normalization',
            fields=[
                ('user', models.OneToOneField(to='instagram.User', serialize=False, primary_key=True)),
                ('data', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to='instagram.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
