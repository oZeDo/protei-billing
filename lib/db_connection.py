from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Query


@event.listens_for(Query, "before_compile", retval=True)
def refresh_info_in_session(query):
    return query.populate_existing()


class DBConnection:
    def __init__(self, host, port, sid, user, paswd):
        self.host = host
        self.port = port
        self.paswd = paswd
        self.user = user
        self.sid = sid
        self.__engine = create_engine(f'oracle+cx_oracle://{self.user}:{self.paswd}@{self.host}:{self.port}/{self.sid}',
                                    echo=False, max_identifier_length=128)
        self.__session = sessionmaker(bind=self.__connect(), autoflush=True)()

    def __connect(self):

        try:
            return self.__engine.connect()
        except Exception as e:
            raise Exception(e)

    @property
    def session(self):
        return self.__session

    def close(self):
        self.session.close()
        self.__engine.dispose()
