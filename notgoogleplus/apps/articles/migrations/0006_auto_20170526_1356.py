# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-26 13:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20170518_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='articlecomment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-created_at']},
        ),
    ]