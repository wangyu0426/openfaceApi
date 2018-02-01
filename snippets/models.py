# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your models here.
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from jsonfield import JSONField

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class FaceData(models.Model):
    identity = models.IntegerField(blank=True)
    rep = JSONField(blank=True)
    phash = models.TextField(primary_key=True,blank=True)
    images = JSONField()
