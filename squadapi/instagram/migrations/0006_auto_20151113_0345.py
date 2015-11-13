# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0005_user_friends_and_family'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('follows_user', models.ForeignKey(related_name='follows_user', to='instagram.User')),
                ('user', models.ForeignKey(related_name='user', to='instagram.User')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set([('user', 'follows_user')]),
        ),
    ]
