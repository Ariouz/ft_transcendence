from django.contrib import admin
from users_service_app.models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id',)
    fields = ('user_id', 'username', 'email', 'token', 'fullname')
    list_display = fields
    search_fields = fields
    list_filter = fields

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    fields = ('user_id', 'avatar', 'display_name', 'lang', 'github', 'status_message')
    list_display = fields
    search_fields = fields
    list_filter = fields

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    fields = ('user', 'friend')
    list_display = fields
    search_fields = fields
    list_filter = fields
