from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User
# Create your models here.
from django import forms


class mailconfig(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    umail = models.EmailField()
    mail_template = models.TextField()
    
    class Admin(admin.ModelAdmin):
        list_display = ('userid', 'umail')



class EmailEditForm(forms.Form):
    username = forms.CharField(max_length=32,required=True,widget=forms.TextInput(attrs={'readonly':'readonly'}))
    umail = forms.EmailField(required=True)
    mailtemplate= forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}))
