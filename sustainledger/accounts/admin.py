from django.contrib import admin
from .models import Profile, Notification, ActivityLog

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'is_read', 'created_at')
    list_filter = ('is_read',)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at')
    ordering = ('-created_at',)
