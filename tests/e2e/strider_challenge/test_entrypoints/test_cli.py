from sqlmodel import Session, create_engine
from typer.testing import CliRunner

from strider_challenge.domain import model
from strider_challenge.entrypoints import cli


def test_app():
    # arrange
    runner = CliRunner()

    # act
    result = runner.invoke(cli.app, ["init-db"])
    assert result.exit_code == 0

    result = runner.invoke(
        cli.app,
        [
            "load",
            "--model",
            "movie",
            "--collector",
            "csv",
            "--config",
            "data/internal/movies.csv",
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        cli.app,
        [
            "load",
            "--model",
            "stream",
            "--collector",
            "csv",
            "--config",
            "data/internal/streams.csv",
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        cli.app,
        [
            "load",
            "--model",
            "user",
            "--collector",
            "csv",
            "--config",
            "data/internal/users.csv",
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        cli.app,
        [
            "load",
            "--model",
            "author",
            "--collector",
            "json",
            "--config",
            "data/vendor/authors.csv",
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        cli.app,
        [
            "load",
            "--model",
            "book",
            "--collector",
            "json",
            "--config",
            "data/vendor/books.csv",
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        cli.app,
        [
            "load",
            "--model",
            "review",
            "--collector",
            "json",
            "--config",
            "data/vendor/reviews.csv",
        ],
    )
    assert result.exit_code == 0

    with Session(create_engine(cli.build_connection_string())) as session:
        counts = [
            session.query(model.Movie).count(),
            session.query(model.Stream).count(),
            session.query(model.User).count(),
            session.query(model.Author).count(),
            session.query(model.Book).count(),
            session.query(model.Review).count(),
        ]

    # assert
    assert min(counts) >= 1
