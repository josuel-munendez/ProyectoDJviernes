"""Configuración del sitio de administración personalizado para el CRM.

Define un panel de administración restringido exclusivamente a superusuarios.
"""
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http import HttpRequest


class SuperuserAdminSite(admin.AdminSite):
    """Sitio de administración que solo permite acceso a superusuarios."""

    def has_permission(self, request: HttpRequest) -> bool:
        """Verifica si el usuario tiene permiso para acceder al panel de administración."""
        return request.user.is_active and request.user.is_superuser


# Instancia del sitio de administración personalizado
admin_site = SuperuserAdminSite(name="superuser_admin")

# Registro de modelos de autenticación de Django
from django.contrib.auth.admin import UserAdmin, GroupAdmin
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Registro de modelos de las aplicaciones del proyecto
from website.models import Record
from usuarios.models import UserProfile
from usuarios.admin import UserProfileAdmin
from productos.models import Producto
from catalogo.models import Categoria, Catalogo

admin_site.register(Record)
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(Producto)
admin_site.register(Categoria)
admin_site.register(Catalogo)
