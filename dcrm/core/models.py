from django.db import models


class BaseModel(models.Model):
    _created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    _updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        abstract = True

    def _get_created_at(self):
        return self._created_at

    def _get_updated_at(self):
        return self._updated_at

    def get_metadata(self):
        return f"Creado: {self._created_at}, Actualizado: {self._updated_at}"
