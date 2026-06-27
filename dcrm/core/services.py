"""Capa de servicios con lógica de negocio para el CRM."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from django.contrib import messages
from django.db.models import Model, QuerySet
from django.http import HttpRequest


class BaseService(ABC):
    """Interfaz abstracta que define las operaciones CRUD estándar."""

    @abstractmethod
    def get_all(self) -> QuerySet:
        """Retorna todos los registros ordenados."""
        pass

    @abstractmethod
    def get_by_id(self, pk: Any) -> Optional[Model]:
        """Obtiene un registro por su id."""
        pass

    @abstractmethod
    def create(self, data: dict) -> Model:
        """Crea un nuevo registro con los datos proporcionados."""
        pass

    @abstractmethod
    def update(self, instance: Model, data: dict) -> Model:
        """Actualiza un registro existente con los datos indicados."""
        pass

    @abstractmethod
    def delete(self, instance: Model) -> None:
        """Elimina un registro de la base de datos."""
        pass


class CrudService(BaseService):
    """Implementación genérica del servicio CRUD usando el ORM de Django."""

    def __init__(self, model_class: type[Model]):
        """Inicializa el servicio con la clase del modelo."""
        self._model_class = model_class

    def get_all(self) -> QuerySet:
        """Retorna todos los registros ordenados por id."""
        return self._model_class.objects.all().order_by("id")

    def get_by_id(self, pk: Any) -> Optional[Model]:
        """Busca un registro por su id; retorna None si no existe."""
        return self._model_class.objects.filter(id=pk).first()

    def create(self, data: dict) -> Model:
        """Crea y retorna un nuevo registro a partir del diccionario de datos."""
        return self._model_class.objects.create(**data)

    def update(self, instance: Model, data: dict) -> Model:
        """Actualiza los campos de la instancia con los valores del diccionario."""
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: Model) -> None:
        """Elimina la instancia de la base de datos."""
        instance.delete()
