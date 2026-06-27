"""Configuración WSGI para el proyecto CRM Django.

Expone la aplicación WSGI como una variable de módulo llamada ``application``.

Para más información, consulta:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')

# Aplicación WSGI para servir el proyecto en producción
application = get_wsgi_application()
