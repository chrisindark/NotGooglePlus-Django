# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-07 15:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20170627_1228'),
        ('posts', '0014_auto_20170707_1513'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postlike',
            unique_together=set([('user', 'post')]),
        ),
    ]
