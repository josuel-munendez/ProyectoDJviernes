"""Configuración del panel de administración para usuarios."""
from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo UserProfile."""

    list_display = ["user", "_rol", "_telefono"]
    list_filter = ["_rol"]
    search_fields = ["user__username", "user__email"]


admin.site.register(UserProfile, UserProfileAdmin)
