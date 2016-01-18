from django.contrib import admin

# Register your models here.
from models import User
from models import Role
from models import UserRole

admin.site.register(User, User.Admin)
admin.site.register(Role, Role.Admin)
admin.site.register(UserRole, UserRole.Admin)