"""Funciones de seguridad y auditoría para el sistema CRM."""

import logging

from django.contrib import messages
from django.http import HttpRequest

logger = logging.getLogger("django.security")


def log_failed_login(request: HttpRequest, username: str) -> None:
    """Registra en el log un intento de inicio de sesión fallido."""
    logger.warning(f"Intento de login fallido para usuario: {username} desde IP: {get_client_ip(request)}")


def log_delete(request: HttpRequest, model_name: str, object_id: int) -> None:
    """Registra en el log la eliminación de un registro por parte de un usuario."""
    logger.info(f"Usuario {request.user.username} eliminó {model_name} id={object_id}")


def get_client_ip(request: HttpRequest) -> str:
    """Obtiene la dirección IP del cliente a partir de la solicitud HTTP.

    Primero intenta con el encabezado X-Forwarded-For (para proxies),
    y luego cae en REMOTE_ADDR.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Toma la primera IP en caso de múltiples saltos de proxy
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "desconocida")


def has_admin_role(user) -> bool:
    """Verifica si el usuario tiene rol de administrador a través de su perfil."""
    from usuarios.models import UserProfile
    try:
        profile = user.profile
        return profile.es_admin()
    except (UserProfile.DoesNotExist, AttributeError):
        # Si no tiene perfil, se verifica si es superusuario
        return user.is_superuser
