import abc
from abc import ABC


class SessionInitializationAbstraction(metaclass=abc.ABCMeta):
    """
    Abstract class for creating session.
    def session property should be created
    """

    def __new__(cls, *args, **kwargs):
        if cls is SessionInitializationAbstraction:
            raise TypeError("TypeError: Can't instantiate abstract class {name} directly".format(name=cls.__name__))
        return object.__new__(cls)

    @property
    @abc.abstractmethod
    def session(self):
        """
        Creates session object based on specified transport layer class

        | Example 1:
        |   @property
        |   def session(self) -> HTTPRequest:
        |      return HTTPRequest(params=self.__params).register_client()
        |
        |
        | Example 2:
        |   def __init__(self):
        |      self.my_session = SomeTransportLayerClass()
        |
        |   @property
        |   def session(self) -> SomeTransportLayerClass:
        |      return self.my_session


        :return: Session object
        """
        raise NotImplementedError


class BaseController(SessionInitializationAbstraction, ABC):
    """
    Базовый контроллер, от которого наследуются все остальные контроллеры.
    Имеет возможность применения декораторов, которые передаются в списке decorators, ко всем публичным методам класса.
    Порядок декорирования метода определяется порядком декораторов в списке decorators.
    У наследованных классов свои методы оборачиваются родительскими и своими декораторами.
    """

    decorators = []

    def __init_subclass__(cls) -> None:
        def combine_decorators(_func, decs):
            for dec in decs:
                _func = dec(_func)
            return _func

        # Получение списка декораторов у всех родительских классов и у самого себя.
        # Как это работает:
        # - из cls.mro() получаем список всех родительских классов + собственный класс, если у него есть свой список decorators
        # - забираем все списки декораторов из всех найденных классов
        # - по порядку разворачиваем списки декораторов в собственный список

        decorators = []
        for c in cls.mro()[int(not "decorators" in cls.__dict__): -1]:
            try:
                for d in c.decorators:
                    decorators.append(d)
            except AttributeError:
                continue

        # Оборачиваем все методы класса, подходящие под условия, в каждый декоратор из списка по порядку.
        for func_name in cls.__dict__:
            if not func_name.startswith("__"):
                func = getattr(cls, func_name)
                if not isinstance(func, property) and callable(func):
                    setattr(cls, func_name, combine_decorators(func, decorators))

        super().__init_subclass__()
