from django.contrib import admin
from .models import (Organization, User)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address']


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'organization', 'birthdate']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(User, UserAdmin)
