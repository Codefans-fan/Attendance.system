from django.db import models

from django.contrib import admin
# Create your models here.



class holiday_cn(models.Model):
    holiday_name = models.CharField(max_length=128)
    day = models.DateField()
    
    class Admin(admin.ModelAdmin):
        list_display = ('holiday_name', 'day')
        
