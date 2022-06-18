import pathlib

from strider_challenge import adapters, service_layer
from strider_challenge.domain import model

DATA_FOLDER = (
    f"{str(pathlib.Path(__file__).parent.parent.parent.parent.resolve())}/data"
)


def test_load_movies(session):
    # arrange
    repo = adapters.SqlRepository(model=model.Movie, session=session)
    collector = adapters.CsvCollector(path=f"{DATA_FOLDER}/internal/movies.csv")

    # act
    service_layer.load_movies(collector=collector, repo=repo)

    # assert
    assert isinstance(repo.get(reference="The Great Escape"), model.Movie)


def test_load_streams(session):
    # arrange
    repo = adapters.SqlRepository(model=model.Stream, session=session)
    collector = adapters.CsvCollector(path=f"{DATA_FOLDER}/internal/streams.csv")

    # act
    service_layer.load_streams(collector=collector, repo=repo)

    # assert
    assert isinstance(
        repo.get(reference="964c33065c01fc45c1a7ab04ad995802ea089c80"), model.Stream
    )


def test_load_users(session):
    # arrange
    repo = adapters.SqlRepository(model=model.User, session=session)
    collector = adapters.CsvCollector(path=f"{DATA_FOLDER}/internal/users.csv")

    # act
    service_layer.load_users(collector=collector, repo=repo)

    # assert
    assert isinstance(repo.get(reference="karine@bode-rogahn.org"), model.User)


def test_load_authors(session):
    # arrange
    repo = adapters.SqlRepository(model=model.Author, session=session)
    collector = adapters.JsonCollector(path=f"{DATA_FOLDER}/internal/authors.json")

    # act
    service_layer.load_authors(collector=collector, repo=repo)

    # assert
    assert isinstance(repo.get(reference="Josh Johnston"), model.Author)


def test_load_books(session):
    # arrange
    repo = adapters.SqlRepository(model=model.Book, session=session)
    collector = adapters.JsonCollector(path=f"{DATA_FOLDER}/internal/books.json")

    # act
    service_layer.load_books(collector=collector, repo=repo)

    # assert
    assert isinstance(repo.get(reference="An Evil Cradling"), model.Book)


def test_load_reviews(session):
    # arrange
    repo = adapters.SqlRepository(model=model.Review, session=session)
    collector = adapters.JsonCollector(path=f"{DATA_FOLDER}/internal/reviews.json")

    # act
    service_layer.load_reviews(collector=collector, repo=repo)

    # assert
    assert isinstance(
        repo.get(reference="8ea86ac9685bafd712fdb89124b56b348d00f13f"), model.Review
    )
