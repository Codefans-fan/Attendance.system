from django.contrib import admin

# Register your models here.
from models import Attend

admin.site.register(Attend, Attend.Admin)