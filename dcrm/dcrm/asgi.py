"""Configuración ASGI para el proyecto CRM Django.

Expone la aplicación ASGI como una variable de módulo llamada ``application``.

Para más información, consulta:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')

# Aplicación ASGI para soporte de conexiones asíncronas
application = get_asgi_application()
