"""Configuración del panel de administración para productos."""
from django.contrib import admin
from .models import Producto

admin.site.register(Producto)
