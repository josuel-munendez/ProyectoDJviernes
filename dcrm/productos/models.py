"""Modelos de la aplicación productos.

Define el modelo Producto con campos de nombre, descripción,
precio, stock y código único.
"""
from django.db import models
from core.models import BaseModel


class Producto(BaseModel):
    """Representa un producto dentro del catálogo del CRM."""

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    codigo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """Representación en cadena del producto."""
        return f"{self.nombre} ({self.codigo})"
