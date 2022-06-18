import csv
import json
from abc import ABC, abstractmethod
from typing import Any, Sequence


class Collector(ABC):
    @abstractmethod
    def collect(self) -> Sequence[dict[str, Any]]:
        """Child class should implement the collection logic and return a json dict."""


class CsvCollector(Collector):
    def __init__(self, path: str):
        self.path = path

    def collect(self) -> Sequence[dict[str, Any]]:
        with open(self.path) as f:
            reader = csv.reader(f, skipinitialspace=True)
            header = next(reader)
            return [dict(zip(header, row)) for row in reader]


class JsonCollector(Collector):
    def __init__(self, path: str):
        self.path = path

    def collect(self) -> Sequence[dict[str, Any]]:
        with open(self.path) as f:
            json_data = json.loads(f.read())
        return json_data if isinstance(json_data, list) else [json_data]
