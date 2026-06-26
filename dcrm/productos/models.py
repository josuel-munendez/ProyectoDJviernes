from django.db import models
from core.models import BaseModel


class Producto(BaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    codigo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
