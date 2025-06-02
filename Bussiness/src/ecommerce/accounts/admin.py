from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-date_joined',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_name', 'country')
    search_filters = ('user__email', 'organization_name')
