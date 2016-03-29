from django.contrib import admin

# Register your models here.
from models import mailconfig
admin.site.register(mailconfig, mailconfig.Admin)