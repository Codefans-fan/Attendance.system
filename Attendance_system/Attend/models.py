from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User
# Create your models here.

class Attend(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    lock_time = models.DateTimeField()
    commet = models.CharField(max_length = 64)
    
    def __unicode__(self):
        return str(self.userId)
    
    class Admin(admin.ModelAdmin):
        list_display = ('userId', 'lock_time', 'commet')
        
    class Meta:
        permissions = (
            ("readall", "Can see all attendance"),
        )