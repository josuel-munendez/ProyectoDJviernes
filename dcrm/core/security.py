import logging

from django.contrib import messages
from django.http import HttpRequest

logger = logging.getLogger("django.security")


def log_failed_login(request: HttpRequest, username: str) -> None:
    logger.warning(f"Intento de login fallido para usuario: {username} desde IP: {get_client_ip(request)}")


def log_delete(request: HttpRequest, model_name: str, object_id: int) -> None:
    logger.info(f"Usuario {request.user.username} eliminó {model_name} id={object_id}")


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "desconocida")


def has_admin_role(user) -> bool:
    from usuarios.models import UserProfile
    try:
        profile = user.profile
        return profile.es_admin()
    except (UserProfile.DoesNotExist, AttributeError):
        return user.is_superuser
