# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-07 15:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20170627_1228'),
        ('articles', '0007_articlelike'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlelike',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='articlelike',
            unique_together=set([('user', 'article')]),
        ),
    ]
