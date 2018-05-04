# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)