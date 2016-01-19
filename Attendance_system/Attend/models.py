from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
from Users.models import User

class Attend(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    lock_time = models.DateTimeField()
    commet = models.CharField(max_length = 64)
    
    class Admin(admin.ModelAdmin):
        list_display = ('userId', 'lock_time', 'commet')