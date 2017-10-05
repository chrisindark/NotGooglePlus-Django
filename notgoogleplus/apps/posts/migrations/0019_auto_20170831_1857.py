# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-31 18:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_auto_20170828_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_file', to='posts.FileUpload'),
        ),
    ]