from django.contrib import admin
from pong_service_app.models import *

# Register your models here.

@admin.register(PongUser)
class PongUserAdmin(admin.ModelAdmin):
    fields = ('user_id', 'game_history', 'last_game')
    list_display = fields
    search_fields = fields
    list_filter = fields

@admin.register(PongGame)
class PongGameAdmin(admin.ModelAdmin):
    readonly_fields = ('game_id',)
    fields = ('game_id', 'users', 'winner_id', 'score', 'type', 'status', 'date', 'map_theme')
    list_display = fields
    search_fields = fields
    list_filter = fields

@admin.register(PongUserStats)
class PongUserStatsAdmin(admin.ModelAdmin):
    fields = ('user_id', 'played', 'wins', 'loses')
    list_display = fields
    search_fields = fields
    list_filter = fields