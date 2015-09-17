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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('post_a', models.ForeignKey(related_name='post_a', to='instagram.Post')),
                ('post_b', models.ForeignKey(related_name='post_b', to='instagram.Post')),
                ('user', models.ForeignKey(to='instagram.User')),
            ],
        ),
        migrations.CreateModel(
            name='PostComparisonQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PostComparisonQueueMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('position', models.IntegerField(default=0)),
                ('comparison', models.ForeignKey(to='instagram.PostComparison')),
                ('queue', models.ForeignKey(to='instagram.PostComparisonQueue')),
            ],
        ),
        migrations.AddField(
            model_name='postcomparisonqueue',
            name='comparisons',
            field=models.ManyToManyField(through='instagram.PostComparisonQueueMember', to='instagram.PostComparison'),
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
