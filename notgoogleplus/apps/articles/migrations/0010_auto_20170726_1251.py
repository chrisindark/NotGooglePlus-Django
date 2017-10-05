# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-26 12:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20170713_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecommentlike',
            name='article_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_comment_l', to='articles.ArticleComment'),
        ),
        migrations.AlterField(
            model_name='articlecommentlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_comment_l', to='profiles.Profile'),
        ),
    ]
