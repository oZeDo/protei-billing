import attr

from models.services.base import BaseModelOperations, convert_to, atr
from lib.utils import Fake


fake = Fake()


@attr.s
class CardGroup(BaseModelOperations):
    clientId: int = atr(converter=convert_to(int))
    name: str = atr(default=fake.name(), converter=str)
    info: str = atr(converter=convert_to(str))
    id: int = atr(eq=False, converter=convert_to(int))
    parentGroupId: int = atr(converter=convert_to(int))


