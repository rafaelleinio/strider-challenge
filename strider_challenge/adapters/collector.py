from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import BaseModel


class Collector(ABC):
    @abstractmethod
    def _collect(self) -> list[dict[str, Any]]:
        pass

    def collect(self, schema: Type[BaseModel]) -> list[BaseModel]:
        pass


class CsvCollector(Collector):
    def __init__(self, path: str):
        self.path = path

    def _collect(self) -> list[dict[str, Any]]:
        pass


class JsonCollector(Collector):
    def __init__(self, path: str):
        self.path = path

    def _collect(self) -> list[dict[str, Any]]:
        pass
