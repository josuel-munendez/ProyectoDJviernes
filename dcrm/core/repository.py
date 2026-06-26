from abc import ABC, abstractmethod
from typing import Any, Optional

from django.db.models import Model, QuerySet


class BaseRepository(ABC):
    @abstractmethod
    def find_all(self) -> QuerySet:
        pass

    @abstractmethod
    def find_by_id(self, pk: Any) -> Optional[Model]:
        pass

    @abstractmethod
    def save(self, instance: Model) -> Model:
        pass

    @abstractmethod
    def remove(self, instance: Model) -> None:
        pass


class DjangoRepository(BaseRepository):
    def __init__(self, model_class: type[Model]):
        self._model_class = model_class

    def find_all(self) -> QuerySet:
        return self._model_class.objects.all()

    def find_by_id(self, pk: Any) -> Optional[Model]:
        return self._model_class.objects.filter(id=pk).first()

    def save(self, instance: Model) -> Model:
        instance.save()
        return instance

    def remove(self, instance: Model) -> None:
        instance.delete()
