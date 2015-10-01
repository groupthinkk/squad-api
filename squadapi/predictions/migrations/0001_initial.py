# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_auto_20150919_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='HIT',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('hit_id', models.CharField(max_length=128, db_index=True)),
                ('status', models.CharField(max_length=64, db_index=True, default='', blank=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('instagram_queue', models.ForeignKey(to='instagram.PostComparisonQueue')),
            ],
        ),
        migrations.CreateModel(
            name='InstagramPrediction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('decision_milliseconds', models.IntegerField()),
                ('correct', models.BooleanField()),
                ('ux_id', models.CharField(max_length=64, default='')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('choice', models.ForeignKey(to='instagram.Post')),
                ('comparison', models.ForeignKey(to='instagram.PostComparison')),
                ('hit', models.ForeignKey(to='predictions.HIT')),
            ],
        ),
        migrations.CreateModel(
            name='Turker',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('turker_id', models.CharField(max_length=128, unique=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='hit',
            name='turker',
            field=models.ForeignKey(to='predictions.Turker', to_field='turker_id'),
        ),
        migrations.AlterUniqueTogether(
            name='instagramprediction',
            unique_together=set([('hit', 'comparison')]),
        ),
        migrations.AlterUniqueTogether(
            name='hit',
            unique_together=set([('hit_id', 'turker'), ('turker', 'instagram_queue')]),
        ),
    ]
