from sqlmodel import Field, Session, SQLModel

from strider_challenge import adapters


class MockSqlModel(SQLModel, table=True):
    name: str = Field(primary_key=True)
    age: int


TARGET = MockSqlModel(name="name", age=18)


class TestSqlRepository:
    def test_add_and_get(self, session: Session):
        # arrange
        repo = adapters.SqlRepository(session=session)

        # act
        repo.add([TARGET])
        output = repo.get(reference="name")

        # assert
        assert output == TARGET
