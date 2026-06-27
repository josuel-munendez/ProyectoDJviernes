"""Modelos base reutilizables para el sistema CRM."""

from django.db import models


class BaseModel(models.Model):
    """Modelo abstracto que provee timestamps automáticos de creación y actualización."""

    _created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    _updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        abstract = True

    def _get_created_at(self):
        """Retorna la fecha de creación del registro."""
        return self._created_at

    def _get_updated_at(self):
        """Retorna la fecha de la última modificación del registro."""
        return self._updated_at

    def get_metadata(self):
        """Devuelve una cadena con las fechas de creación y actualización."""
        return f"Creado: {self._created_at}, Actualizado: {self._updated_at}"
