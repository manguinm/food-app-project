# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-10 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0018_recipe_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ranking',
            field=models.FloatField(default=5),
        ),
    ]
