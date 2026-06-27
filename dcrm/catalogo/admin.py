"""Configuración del panel de administración para catálogo."""
from django.contrib import admin
from .models import Categoria, Catalogo

admin.site.register(Categoria)
admin.site.register(Catalogo)
