"""Configuracion del panel de administracion de Django para la aplicacion website."""

from django.contrib import admin

from .models import Record


# Registra el modelo Record en el panel de administracion
admin.site.register(Record)
