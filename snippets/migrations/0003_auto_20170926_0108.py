# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 01:08
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_facedata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Snippet',
        ),
        migrations.AlterField(
            model_name='facedata',
            name='rep',
            field=jsonfield.fields.JSONField(),
        ),
    ]
