# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 20:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0006_auto_20170220_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredient_id',
        ),
    ]