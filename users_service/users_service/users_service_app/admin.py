from django.contrib import admin
from users_service_app.models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'token')  # Champs à afficher dans la liste
    search_fields = ('id', 'username', 'email', 'token')  # Champs pour la barre de recherche
    list_filter = ('id', 'username', 'email', 'token')  # Filtres disponibles sur le côté
