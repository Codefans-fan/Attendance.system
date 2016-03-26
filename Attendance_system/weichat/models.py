from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

from django.forms import ModelForm
from django import forms


from itertools import chain
class  user_weichat(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    weichatname = models.CharField(max_length = 64)
    
    class Admin(admin.ModelAdmin):
        list_display = ('userid', 'weichatname')
    


class edit_form(ModelForm):
    def __init__(self, uid, *args, **kwargs):
        super(edit_form, self).__init__(*args, **kwargs)
        
    class Meta:
        model = user_weichat
        fields = ('userid', 'weichatname')  
