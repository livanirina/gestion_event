from django.contrib import admin
from .models import Utilisateur, Evenement, Reservation, Commentaire

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')  # Utiliser les champs par défaut si `is_admin` n'est pas nécessaire
    search_fields = ('username', 'email')

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Evenement)
admin.site.register(Reservation)
admin.site.register(Commentaire)
