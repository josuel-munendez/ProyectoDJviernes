#!/usr/bin/env python3
"""Wrapper para ejecutar comandos de administración de Django desde la raíz del proyecto."""
import os
import sys

if __name__ == "__main__":
    # Cambia al directorio dcrm y lo añade al PATH antes de ejecutar comandos
    os.chdir(os.path.join(os.path.dirname(__file__), "dcrm"))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dcrm"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcrm.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
