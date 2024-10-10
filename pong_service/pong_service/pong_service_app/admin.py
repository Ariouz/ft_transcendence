from django.contrib import admin
from pong_service_app.models import *

# Register your models here.

@admin.register(PongUser)
class PongUserAdmin(admin.ModelAdmin):
    fields = ('user_id', 'game_history')
    list_display = fields
    search_fields = fields
    list_filter = fields

@admin.register(PongGame)
class PongGameAdmin(admin.ModelAdmin):
    fields = ('users', 'winner_id', 'score', 'type')
    list_display = fields
    search_fields = fields
    list_filter = fields

@admin.register(PongUserStats)
class PongUserStatsAdmin(admin.ModelAdmin):
    fields = ('user_id', 'played', 'wins', 'loses')
    list_display = fields
    search_fields = fields
    list_filter = fields