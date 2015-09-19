# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_squashed_0004_auto_20150731_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComparison',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('post_a', models.ForeignKey(related_name='post_a', to='instagram.Post')),
                ('post_b', models.ForeignKey(related_name='post_b', to='instagram.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostComparisonQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PostComparisonQueueMember',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('comparison', models.ForeignKey(to='instagram.PostComparison')),
                ('queue', models.ForeignKey(to='instagram.PostComparisonQueue')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='', blank=True, unique=True, max_length=64),
        ),
        migrations.AddField(
            model_name='postcomparisonqueue',
            name='comparisons',
            field=models.ManyToManyField(to='instagram.PostComparison', through='instagram.PostComparisonQueueMember'),
        ),
        migrations.AddField(
            model_name='postcomparison',
            name='user',
            field=models.ForeignKey(to='instagram.User'),
        ),
        migrations.AlterUniqueTogether(
            name='postcomparisonqueuemember',
            unique_together=set([('queue', 'comparison')]),
        ),
        migrations.AlterUniqueTogether(
            name='postcomparison',
            unique_together=set([('post_a', 'post_b')]),
        ),
    ]
