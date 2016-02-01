from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User
# Create your models here.

class Attend(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    lock_time = models.DateTimeField()
    comment = models.CharField(max_length = 64)
    
    def to_dict(self):
        return {'uid':self.userId,'lock_time':self.lock_time,'comment':self.comment}
    
    def __unicode__(self):
        return str(self.userId)
    
    class Admin(admin.ModelAdmin):
        list_display = ('userId', 'lock_time', 'comment')
        
    class Meta:
        permissions = (
            ("readall", "Can see all attendance"),
        )