#!/usr/bin/env python3
"""Wrapper to run Django management commands from the project root."""
import os
import sys

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "dcrm"))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dcrm"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcrm.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
