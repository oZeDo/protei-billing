import pytest
from sqlalchemy import create_engine, event, delete, insert, select, update
from sqlalchemy.orm import Session, Query
from sqlalchemy.pool import QueuePool

# For type hinting
from sqlalchemy.sql.dml import Delete, Insert, Update
from sqlalchemy.sql.selectable import Select
from models.database.reflected_db import Base


@event.listens_for(Query, "before_compile", retval=True)
def refresh_info_in_session(query):
    return query.populate_existing()


class DBSession:

    session_type = Session

    def __init__(self, url: str, pool_size: int = 5, max_overflow: int = 5):
        """Database session costructor

        Args:
            url (str): Database connection string (DSN). Exmaple format: {DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SID}
            pool_size (int, optional): Number of connections to be maintained. Defaults to 5.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults to 5.
        """
        self.__engine = create_engine(url,
                                      poolclass=QueuePool,
                                      pool_size=pool_size,
                                      max_overflow=max_overflow)

        self.__session = Session(self.__engine, future=True)

    def close(self):
        self.__session.close()
        self.__engine.dispose()

    def execute(self, statement, **kwargs):
        return self.__session.execute(statement, **kwargs)

    def query(self, *entities, **kwargs) -> Query:
        return self.__session.query(*entities, **kwargs)

    def add(self, instance):
        self.__session.add(instance)

    # def commit_changes(self, mark_as_failed=False):
    #     try:
    #         self.__session.commit()
    #     except:
    #         self.__session.rollback()
    #         if mark_as_failed:
    #             pytest.xfail('Couldn\'t commit changes to the database. Test failed.')
    #         else:
    #             pytest.skip('Couldn\'t commit changes to the database. Test skipped.')

    def commit(self):
        self.__session.commit()

    def update(self, entity: Base) -> Update:
        return update(entity)

    def insert(self, entity: Base) -> Insert:
        return insert(entity)

    def delete(self, entity: Base) -> Delete:
        return delete(entity)

    def select(self, entity: Base) -> Select:
        return select(entity)
