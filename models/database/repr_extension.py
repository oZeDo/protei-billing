class ReprExtension(object):
    @property
    def as_dict(self) -> dict:
        return self.__items_to_dict()

    @property
    def as_values(self) -> list:
        return self.__items_to_values_list()

    def __repr__(self) -> str:
        return self.__to_str()

    def __str__(self) -> str:
        return self.__to_str()

    def __to_str(self) -> str:
        return ":".join([self.__class__.__name__, str(self.__items_to_dict())])

    def __items_to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __items_to_values_list(self):
        return [f"{k} = {v}" for k, v in self.__dict__.items() if not k.startswith("_")]
