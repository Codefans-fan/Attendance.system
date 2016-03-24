from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

from django import forms


import wechat_utils

class  user_weichat(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    weichatname = models.CharField(max_length = 64)
    
    class Admin(admin.ModelAdmin):
        list_display = ('userid', 'weichatname')
    


class WechatEditForm(forms.Form):
    username = forms.CharField(max_length=32,required=True,widget=forms.TextInput(attrs={'readonly':'readonly'}))
    shortname = forms.CharField(max_length=16,required=True)
    
    def __init__(self, readonly_shortname=False, *args, **kwargs):
        super(WechatEditForm, self).__init__(*args, **kwargs)
        if readonly_shortname:
            self.fields['shortname'].widget.attrs['readonly'] = True
            
    def clean(self):
        cleaned_data = super(WechatEditForm, self).clean()
        shortname = cleaned_data.get("shortname")
        token = wechat_utils.get_weichat_token()
        if not wechat_utils.validate_weichat_user(shortname,token):
            #validate failed
            self.add_error('shortname','wechat validate error. Please ensure you have follow DSA account.')                                                            
        