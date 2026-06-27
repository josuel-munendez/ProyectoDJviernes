"""Etiquetas de plantilla personalizadas para la navegacion del CRM.

Proporciona etiquetas para resaltar enlaces activos y
verificar roles de usuario en las plantillas.
"""

from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, url_name):
    """Retorna 'active' si la URL actual coincide con el nombre proporcionado."""
    request: HttpRequest = context.get("request")
    if request and request.resolver_match and request.resolver_match.url_name == url_name:
        return "active"
    return ""


@register.simple_tag(takes_context=True)
def user_has_role(context, *roles):
    """Verifica si el usuario autenticado tiene alguno de los roles especificados."""
    request = context.get("request")
    if not request or not request.user.is_authenticated:
        return False
    try:
        profile = request.user.profile
        return profile.rol in roles
    except Exception:
        return False


@register.simple_tag(takes_context=True)
def user_is_superuser(context):
    """Verifica si el usuario autenticado es superusuario."""
    request = context.get("request")
    return request and request.user.is_authenticated and request.user.is_superuser
