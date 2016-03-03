from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class  user_weichat(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    weichatname = models.CharField(max_length = 64)