import pathlib
from typing import Any

from pydantic import BaseModel

from strider_challenge import adapters

DATA = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
PATH = str(pathlib.Path(__file__).parent.resolve())


class MockModel(BaseModel):
    x: int
    y: int


class MockCollector(adapters.Collector):
    def collect(self) -> list[dict[str, Any]]:
        return DATA


class TestCsvCollector:
    def test__collect(self):
        # arrange
        collector = adapters.CsvCollector(path=f"{PATH}/data.csv")

        # act
        output = collector.collect()

        # assert
        assert output == [{k: str(v) for k, v in d.items()} for d in DATA]


class TestJsonCollector:
    def test__collect(self):
        # arrange
        collector = adapters.JsonCollector(path=f"{PATH}/data.json")

        # act
        output = collector.collect()

        # assert
        assert output == DATA
