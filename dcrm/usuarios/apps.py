"""Configuración de la aplicación usuarios."""
from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """Configuración de la aplicación de usuarios."""

    name = 'usuarios'

    def ready(self):
        """Importa las señales al iniciar la aplicación."""
        import usuarios.signals  # noqa
