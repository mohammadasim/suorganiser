from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    """
    Custom user admin for user model
    """
    pass


admin.site.register(User, UserAdmin)
