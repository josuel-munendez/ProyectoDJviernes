from abc import ABC, abstractmethod
from typing import Any, Optional

from django.contrib import messages
from django.db.models import Model, QuerySet
from django.http import HttpRequest


class BaseService(ABC):
    @abstractmethod
    def get_all(self) -> QuerySet:
        pass

    @abstractmethod
    def get_by_id(self, pk: Any) -> Optional[Model]:
        pass

    @abstractmethod
    def create(self, data: dict) -> Model:
        pass

    @abstractmethod
    def update(self, instance: Model, data: dict) -> Model:
        pass

    @abstractmethod
    def delete(self, instance: Model) -> None:
        pass


class CrudService(BaseService):
    def __init__(self, model_class: type[Model]):
        self._model_class = model_class

    def get_all(self) -> QuerySet:
        return self._model_class.objects.all().order_by("id")

    def get_by_id(self, pk: Any) -> Optional[Model]:
        return self._model_class.objects.filter(id=pk).first()

    def create(self, data: dict) -> Model:
        return self._model_class.objects.create(**data)

    def update(self, instance: Model, data: dict) -> Model:
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: Model) -> None:
        instance.delete()
