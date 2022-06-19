import abc
from typing import Sequence, Type

from sqlalchemy.inspection import inspect
from sqlmodel import Session, SQLModel, select
from sqlmodel.sql.expression import Select, SelectOfScalar

# supress warnings 😔 from issue: https://github.com/tiangolo/sqlmodel/issues/189
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


class AbstractRepository(abc.ABC):
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    @abc.abstractmethod
    def _add(self, records: Sequence[SQLModel]) -> None:
        """Child class should implement add command logic."""

    def add(self, records: Sequence[SQLModel]) -> None:
        self._add(records)

    @abc.abstractmethod
    def _get(self, reference: str) -> SQLModel | None:
        """Child class should implement get command logic."""

    def get(self, reference: str) -> SQLModel | None:
        return self._get(reference)


class SqlRepository(AbstractRepository):
    def __init__(self, model: Type[SQLModel], session: Session, pk: str | None = None):
        super().__init__(model)
        self.session = session
        self.pk = pk or inspect(model).primary_key[0].name

    def _add(self, records: Sequence[SQLModel]) -> None:
        for record in records:
            new_record = self._get(reference=getattr(record, self.pk)) or record
            for key, value in record.dict().items():
                setattr(new_record, key, value)
            self.session.add(new_record)
        self.session.commit()

    def _get(self, reference: str) -> SQLModel | None:
        statement = select(self.model).where(getattr(self.model, self.pk) == reference)
        return self.session.exec(statement).first()
