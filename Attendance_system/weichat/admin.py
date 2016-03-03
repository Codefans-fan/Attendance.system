from django.contrib import admin

# Register your models here.
from models import user_weichat
admin.site.register(user_weichat, user_weichat.Admin)