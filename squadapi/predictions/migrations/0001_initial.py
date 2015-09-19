# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0004_auto_20150919_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramPrediction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('decision_milliseconds', models.IntegerField()),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('choice', models.ForeignKey(to='instagram.Post', to_field='post_id')),
                ('comparison', models.ForeignKey(to='instagram.PostComparisonQueueMember')),
            ],
        ),
        migrations.CreateModel(
            name='Turker',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('turker_id', models.CharField(max_length=128, unique=True)),
                ('instagram_queue', models.ForeignKey(null=True, blank=True, to='instagram.PostComparisonQueue')),
            ],
        ),
        migrations.AddField(
            model_name='instagramprediction',
            name='turker',
            field=models.ForeignKey(to='predictions.Turker'),
        ),
    ]
