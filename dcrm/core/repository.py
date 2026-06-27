"""Patrón repositorio para abstraer el acceso a datos del CRM."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from django.db.models import Model, QuerySet


class BaseRepository(ABC):
    """Interfaz abstracta para el patrón repositorio."""

    @abstractmethod
    def find_all(self) -> QuerySet:
        """Retorna todos los registros del modelo."""
        pass

    @abstractmethod
    def find_by_id(self, pk: Any) -> Optional[Model]:
        """Busca un registro por su identificador primario."""
        pass

    @abstractmethod
    def save(self, instance: Model) -> Model:
        """Persiste una instancia en la base de datos."""
        pass

    @abstractmethod
    def remove(self, instance: Model) -> None:
        """Elimina una instancia de la base de datos."""
        pass


class DjangoRepository(BaseRepository):
    """Implementación concreta del repositorio usando el ORM de Django."""

    def __init__(self, model_class: type[Model]):
        """Inicializa el repositorio con la clase del modelo a gestionar."""
        self._model_class = model_class

    def find_all(self) -> QuerySet:
        """Retorna todos los objetos del modelo."""
        return self._model_class.objects.all()

    def find_by_id(self, pk: Any) -> Optional[Model]:
        """Busca un objeto por su id; retorna None si no existe."""
        return self._model_class.objects.filter(id=pk).first()

    def save(self, instance: Model) -> Model:
        """Guarda la instancia en la base de datos y la retorna."""
        instance.save()
        return instance

    def remove(self, instance: Model) -> None:
        """Elimina la instancia de la base de datos."""
        instance.delete()
