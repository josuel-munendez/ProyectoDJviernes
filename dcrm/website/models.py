"""Modelos de datos para la aplicacion website.

Define el modelo principal Record para almacenar
informacion de clientes en el sistema CRM.
"""

from django.db import models
from core.models import BaseModel


class Record(BaseModel):
    """Representa un registro de cliente en el CRM.

    Almacena datos personales y de contacto como nombre,
    correo electronico, telefono y direccion.
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        """Representacion en cadena del registro con nombre, apellido y email."""
        return f"{self.first_name} {self.last_name} {self.email}"

    def full_name(self):
        """Retorna el nombre completo del cliente."""
        return f"{self.first_name} {self.last_name}"

    def get_contact_info(self):
        """Retorna informacion de contacto del cliente (email y telefono)."""
        return f"Email: {self.email}, Tel: {self.phone}"
