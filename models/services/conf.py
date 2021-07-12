from typing import TypeVar, Any


T = TypeVar('T')


class MissingType(object):
    def __repr__(self) -> str:
        return 'MISSING'

    def __copy__(self) -> T:
        return self

    def __deepcopy__(self: T, _: Any) -> T:
        return self


MISSING = MissingType()

if __name__ == '__main__':
    print(MISSING)
