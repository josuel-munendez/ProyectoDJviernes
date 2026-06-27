"""Modelos de la aplicación catálogo.

Define las categorías y los catálogos que agrupan productos
dentro del sistema CRM.
"""
from django.db import models
from core.models import BaseModel


class Categoria(BaseModel):
    """Categoría temática para agrupar catálogos de productos."""

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        """Representación en cadena de la categoría."""
        return self.nombre


class Catalogo(BaseModel):
    """Agrupación de productos dentro de una categoría específica."""

    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="catalogos")
    producto = models.ForeignKey("productos.Producto", on_delete=models.CASCADE, related_name="catalogos")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Catalogos"

    def __str__(self):
        """Representación en cadena del catálogo."""
        return f"{self.nombre} - {self.producto.nombre}"
