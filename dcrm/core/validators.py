"""Validadores de campos mediante expresiones regulares para el CRM."""

import re


class RegexValidator:
    """Valida campos comunes (usuario, email, teléfono, etc.) usando patrones regex predefinidos."""

    _patterns = {
        "username": re.compile(r"^[a-zA-Z0-9@\.\+\-_]+$"),
        "name": re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"),
        "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
        "phone": re.compile(r"^\+?\d{7,15}$"),
        "password": re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&_]{8,}$"),
        "zip_code": re.compile(r"^\d{4,10}$"),
    }

    @classmethod
    def validate(cls, field_type: str, value: str) -> bool:
        """Valida un valor contra el patrón correspondiente al tipo de campo.

        Si el tipo de campo no está registrado, retorna True.
        """
        pattern = cls._patterns.get(field_type)
        if pattern is None:
            return True
        return bool(pattern.match(value))
