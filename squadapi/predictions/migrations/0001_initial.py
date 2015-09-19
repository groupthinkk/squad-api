# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_auto_20150919_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramPrediction',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('decision_milliseconds', models.IntegerField()),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('choice', models.ForeignKey(to='instagram.Post')),
                ('comparison', models.ForeignKey(to='instagram.PostComparisonQueueMember')),
            ],
        ),
        migrations.CreateModel(
            name='Turker',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('turker_id', models.CharField(unique=True, max_length=128)),
                ('instagram_queue', models.ForeignKey(blank=True, null=True, to='instagram.PostComparisonQueue')),
            ],
        ),
        migrations.AddField(
            model_name='instagramprediction',
            name='turker',
            field=models.ForeignKey(to='predictions.Turker'),
        ),
        migrations.AlterUniqueTogether(
            name='instagramprediction',
            unique_together=set([('turker', 'comparison')]),
        ),
    ]
