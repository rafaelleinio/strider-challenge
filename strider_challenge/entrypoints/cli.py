import os
from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from sqlalchemy.future import Engine as _FutureEngine
from sqlmodel import Session, SQLModel, create_engine

from strider_challenge import service_layer

app = typer.Typer()


def _build_connection_string() -> str:
    return os.environ.get("DATABASE_URL", "sqlite:///database.db")


def _build_engine() -> _FutureEngine:
    return create_engine(_build_connection_string())


@app.command()
def init_db() -> None:
    """Initialize the database with all models declared in domain."""
    SQLModel.metadata.create_all(_build_engine())


class ModelEnum(str, Enum):
    """Possible choices for models."""

    movie = "movie"
    stream = "stream"
    user = "user"
    author = "author"
    book = "book"
    review = "review"


MODEL_ENUM_MAP = {
    ModelEnum.movie: service_layer.load_movies,
    ModelEnum.stream: service_layer.load_streams,
    ModelEnum.user: service_layer.load_users,
    ModelEnum.author: service_layer.load_authors,
    ModelEnum.book: service_layer.load_books,
    ModelEnum.review: service_layer.load_reviews,
}


class CollectorEnum(str, Enum):
    """Possible choice for collectors."""

    csv = "csv"
    json = "json"


COLLECTOR_ENUM_MAP = {
    CollectorEnum.csv: service_layer.adapters.CsvCollector,
    CollectorEnum.json: service_layer.adapters.JsonCollector,
}


@app.command()
def load(
    model: ModelEnum = typer.Option(ModelEnum.movie),
    collector: CollectorEnum = typer.Option(CollectorEnum.csv),
    config: Optional[Path] = typer.Option(None),
) -> None:
    """Extract, transform, and load records into a specific model repository.

    Args:
        model: what model to populate.
        collector: what collector to use.
        config: arg for the collector (path to file).

    """
    with Session(_build_engine()) as session:
        service = MODEL_ENUM_MAP[model]
        collector_cls = COLLECTOR_ENUM_MAP[collector]
        service(collector=collector_cls(path=str(config)), session=session)


if __name__ == "__main__":
    app()
