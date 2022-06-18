import abc

from sqlmodel import Session, SQLModel


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def _add(self, models: list[SQLModel]) -> None:
        """Child class should implement add command logic."""

    def add(self, models: list[SQLModel]) -> None:
        self._add(models)

    @abc.abstractmethod
    def _get(self, reference: str) -> SQLModel:
        """Child class should implement get command logic."""

    def get(self, reference: str) -> SQLModel:
        return self._get(reference)


class SqlRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def _add(self, model: list[SQLModel]) -> None:
        pass

    def _get(self, reference: str) -> SQLModel:
        pass
