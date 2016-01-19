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
    last_login = models.DateField(blank=True,default=django.utils.timezone.now)
    def __str__(self):
        return self.name
    
    class Admin(admin.ModelAdmin):
        list_display = ('name', 'display_name', 'email')
        list_filter = ('name', )
        ordering = ('-create_date',)
        
class Role(models.Model):
    roleKey = models.IntegerField()
    roleName = models.CharField(max_length=64)
    
    def __str__(self):
        return self.roleName
    
    class Admin(admin.ModelAdmin):
        list_display = ('roleKey', 'roleName')
    
class UserRole(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    roleId = models.ForeignKey(Role,on_delete=models.CASCADE)
    
    class Admin(admin.ModelAdmin):
        list_display = ('userId', 'roleId')
    
    
    