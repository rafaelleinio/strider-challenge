from strider_challenge import adapters


def _creat_default_repository() -> adapters.AbstractRepository:
    pass


def load_movies(
    collector: adapters.Collector,
    repo: adapters.AbstractRepository | None = None,
) -> None:
    pass


def load_streams(
    collector: adapters.Collector, repo: adapters.AbstractRepository | None = None
) -> None:
    pass


def load_users(
    collector: adapters.Collector, repo: adapters.AbstractRepository | None = None
) -> None:
    pass


def load_authors(
    collector: adapters.Collector, repo: adapters.AbstractRepository | None = None
) -> None:
    pass


def load_books(
    collector: adapters.Collector, repo: adapters.AbstractRepository | None = None
) -> None:
    pass


def load_reviews(
    collector: adapters.Collector, repo: adapters.AbstractRepository | None = None
) -> None:
    pass
