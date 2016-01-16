from __future__ import unicode_literals

from django.db import models

# Create your models here.
import django.utils
from django.contrib import admin

class User(models.Model):
    name = models.CharField(max_length=32)
    display_name = models.CharField(max_length=64)
    password = models.CharField(max_length = 64)
    email = models.EmailField()
    create_date = models.DateField(blank=True,default=django.utils.timezone.now)
    def __str__(self):
        return self.name
    
    class Admin(admin.ModelAdmin):
        list_display = ('name', 'display_name', 'email')
        list_filter = ('name', )
        ordering = ('-create_date',)
        


class Role(models.Model):        
    roleID = models.IntegerField(max_length=32)
    roleName = models.CharField(max_length=64)
    
    
class UserRole(models.Model):
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    roleID = models.ForeignKey(User,on_delete=models.CASCADE)