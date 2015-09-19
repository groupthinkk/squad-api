# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0003_remove_postcomparisonqueuemember_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomparison',
            name='post_a',
            field=models.ForeignKey(related_name='post_a', to_field='post_id', to='instagram.Post'),
        ),
        migrations.AlterField(
            model_name='postcomparison',
            name='post_b',
            field=models.ForeignKey(related_name='post_b', to_field='post_id', to='instagram.Post'),
        ),
    ]
