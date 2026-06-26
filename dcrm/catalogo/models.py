from django.db import models
from core.models import BaseModel


class Categoria(BaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


class Catalogo(BaseModel):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="catalogos")
    producto = models.ForeignKey("productos.Producto", on_delete=models.CASCADE, related_name="catalogos")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Catalogos"

    def __str__(self):
        return f"{self.nombre} - {self.producto.nombre}"
