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

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    readonly_fields = ('tournament_id',)
    fields = ('tournament_id', 'state', 'winner', 'host', 'created_at')
    list_display = fields
    search_fields = fields
    list_filter = fields

@admin.register(TournamentParticipant)
class TournamentParticipantAdmin(admin.ModelAdmin):
    fields = ('tournament', 'pong_user', 'eliminated')
    list_display = fields
    search_fields = fields
    list_filter = fields

@admin.register(TournamentMatch)
class TournamentMatchAdmin(admin.ModelAdmin):
    fields = ('tournament', 'player1', 'player2', 'winner', 'round', 'score1', 'score2')
    list_display = fields
    search_fields = fields
    list_filter = fields