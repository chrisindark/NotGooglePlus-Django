# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-13 20:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20170414_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='OauthAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=32)),
                ('access_token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('id_token', models.CharField(max_length=255)),
                ('expires_in', models.DateTimeField()),
                ('token_type', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oauth', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]