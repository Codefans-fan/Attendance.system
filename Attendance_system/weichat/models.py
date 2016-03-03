from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

class  user_weichat(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    weichatname = models.CharField(max_length = 64)
    
    class Admin(admin.ModelAdmin):
        list_display = ('userid', 'weichatname')
        