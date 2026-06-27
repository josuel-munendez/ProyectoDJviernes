"""Middleware de seguridad que agrega cabeceras HTTP protectivas."""

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware que inyecta cabeceras de seguridad en todas las respuestas HTTP."""

    def process_response(self, request, response):
        """Agrega cabeceras de seguridad a la respuesta antes de enviarla al cliente."""
        if isinstance(response, HttpResponse):
            response["X-Content-Type-Options"] = "nosniff"
            response["X-Frame-Options"] = "DENY"
            response["X-XSS-Protection"] = "1; mode=block"
            response["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response
