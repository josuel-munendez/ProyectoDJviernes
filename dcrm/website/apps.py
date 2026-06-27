"""Configuracion de la aplicacion website para Django."""

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """Configuracion de la aplicacion website del CRM."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'
