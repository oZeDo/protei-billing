from dataclasses import dataclass, field, asdict


@dataclass
class TransportParams:
    base_url: str
    endpoint: str = field(default_factory='')
    headers: dict = field(default_factory={})
    cookies: dict = field(default_factory={})

    def __post_init__(self):
        self.endpoint = '' if self.endpoint is None else self.endpoint
        self.headers = {} if self.headers is None else self.headers
        self.cookies = {} if self.cookies is None else self.cookies

    def as_dict(self):
        return asdict(self)


@dataclass
class DBParams:
    host: str
    port: str
    paswd: str
    user: str
    sid: str


"""
self.__engine = create_engine(f'oracle+cx_oracle://{self.user}:{self.paswd}@{self.host}:{self.port}/{self.sid}',
                              echo=False, max_identifier_length=128)
self.__session = sessionmaker(bind=self.__connect(), autoflush=True)()
"""
