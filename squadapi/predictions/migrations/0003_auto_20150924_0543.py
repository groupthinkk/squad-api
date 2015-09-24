# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_auto_20150919_2112'),
        ('predictions', '0002_auto_20150922_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='HIT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('hit_id', models.CharField(db_index=True, max_length=128)),
                ('status', models.CharField(default='', blank=True, db_index=True, max_length=64)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('instagram_queue', models.ForeignKey(to='instagram.PostComparisonQueue')),
            ],
        ),
        migrations.RemoveField(
            model_name='turker',
            name='instagram_queue',
        ),
        migrations.AlterField(
            model_name='instagramprediction',
            name='comparison',
            field=models.ForeignKey(to='instagram.PostComparison'),
        ),
        migrations.AlterUniqueTogether(
            name='instagramprediction',
            unique_together=set([('hit', 'comparison')]),
        ),
        migrations.AddField(
            model_name='hit',
            name='turker',
            field=models.ForeignKey(to_field='turker_id', to='predictions.Turker'),
        ),
        migrations.RemoveField(
            model_name='instagramprediction',
            name='turker',
        ),
        migrations.AddField(
            model_name='instagramprediction',
            name='hit',
            field=models.ForeignKey(default=0, to='predictions.HIT'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='hit',
            unique_together=set([('turker', 'instagram_queue'), ('hit_id', 'turker')]),
        ),
    ]
