from enum import Enum
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()


def build_connection_string() -> str:
    return "sqlite:///database.db"


@app.command()
def init_db() -> None:
    pass


class ModelEnum(str, Enum):
    movie = "movie"
    stream = "stream"
    user = "user"
    author = "author"
    book = "book"
    review = "review"


class CollectorEnum(str, Enum):
    csv = "csv"
    json = "json"


@app.command()
def load(
    model: ModelEnum = typer.Option(ModelEnum.movie),
    collector: CollectorEnum = typer.Option(CollectorEnum.csv),
    config: Optional[Path] = typer.Option(None),
) -> None:
    pass


if __name__ == "__main__":
    app()
