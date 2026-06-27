"""Define las rutas URL principales del proyecto CRM Django."""
from django.urls import path, include
from django.conf.urls import handler404, handler500

from .admin import admin_site

# Mapeo de rutas URL a las aplicaciones del proyecto
urlpatterns = [
    # Panel de administración personalizado (solo superusuarios)
    path('admin/', admin_site.urls),
    # Rutas de autenticación y gestión de usuarios
    path('', include('usuarios.urls')),
    # Rutas del sitio web principal
    path('', include('website.urls')),
    # Rutas del módulo de productos
    path('productos/', include('productos.urls')),
    # Rutas del módulo de catálogo
    path('catalogo/', include('catalogo.urls')),
]