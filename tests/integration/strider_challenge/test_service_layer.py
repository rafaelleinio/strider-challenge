import pathlib

import pytest

from strider_challenge import adapters, service_layer
from strider_challenge.domain import model

DATA_FOLDER = (
    f"{str(pathlib.Path(__file__).parent.parent.parent.parent.resolve())}/data"
)


@pytest.mark.parametrize(
    "model_cls, service, collector, reference",
    [
        (
            model.Movie,
            service_layer.load_movies,
            adapters.CsvCollector(path=f"{DATA_FOLDER}/internal/movies.csv"),
            "The Great Escape",
        ),
        (
            model.Stream,
            service_layer.load_streams,
            adapters.CsvCollector(path=f"{DATA_FOLDER}/internal/streams.csv"),
            "964c33065c01fc45c1a7ab04ad995802ea089c80",
        ),
        (
            model.User,
            service_layer.load_users,
            adapters.CsvCollector(path=f"{DATA_FOLDER}/internal/users.csv"),
            "karine@bode-rogahn.org",
        ),
        (
            model.Author,
            service_layer.load_authors,
            adapters.JsonCollector(path=f"{DATA_FOLDER}/vendor/authors.json"),
            "Josh Johnston",
        ),
        (
            model.Book,
            service_layer.load_books,
            adapters.JsonCollector(path=f"{DATA_FOLDER}/vendor/books.json"),
            "An Evil Cradling",
        ),
        (
            model.Review,
            service_layer.load_reviews,
            adapters.JsonCollector(path=f"{DATA_FOLDER}/vendor/reviews.json"),
            "8ea86ac9685bafd712fdb89124b56b348d00f13f",
        ),
    ],
)
def test_load(model_cls, service, collector, reference, session):
    # arrange
    repo = adapters.SqlRepository(model=model_cls, session=session)

    # act
    service(collector=collector, repo=repo)

    # assert
    assert isinstance(repo.get(reference=reference), model_cls)
