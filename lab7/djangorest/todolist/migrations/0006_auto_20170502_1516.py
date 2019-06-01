# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 12:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todolist', '0005_share_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='username',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='share',
            unique_together=set([('username', 'tasklist')]),
        ),
    ]
