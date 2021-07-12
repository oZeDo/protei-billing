import json
from typing import Type, ClassVar, Mapping, NoReturn, TypeVar, Dict, Any

import attr
import cattr
import xmltodict

from models.services.conf import MISSING, MissingType

T = TypeVar('T')  # pylint: disable=invalid-name


def convert_to(convert, *args, **kwargs):
    def opt_conv(value):
        if isinstance(value, MissingType):
            return value
        elif value is None:
            return MISSING
        return convert(value)

    return opt_conv


def atr(default=MISSING, eq=True, converter=None, **kwargs):
    return attr.ib(*kwargs, default=default, converter=converter, eq=eq)


class BaseConverter(cattr.Converter):
    def __init__(self):
        self.MISSING = MISSING
        super().__init__()
        # Extend with custom hooks for types

    @staticmethod
    def __raise_error_for_unexpected_args(obj: Mapping, cl: Type[T]) -> NoReturn:
        for k in obj.keys():
            if k not in (x.name for x in cl.__attrs_attrs__):
                raise KeyError(
                    f" {cl.__name__} has no parameter {k}. {[x.name for x in cl.__attrs_attrs__]}")

    def structure_attrs_fromdict(self, obj: Mapping, cl: Type[T], *, ignore_extra_args=False) -> T:
        """Instantiate an attrs class from a mapping.
        Raises human-readable StructureError exceptions on failure.
        """

        if ignore_extra_args is False:
            BaseConverter.__raise_error_for_unexpected_args(obj, cl)

        conv_obj = {}
        dispatch = self._structure_func.dispatch
        for a in cl.__attrs_attrs__:
            type_ = a.type
            name = a.name

            try:
                val = obj[name]
            except KeyError:
                val = self.MISSING
                type_ = None

            if name[0] == "_":
                name = name[1:]

            conv_obj[name] = (
                dispatch(type_)(val, type_) if type_ is not None else val
            )

        return cl(**conv_obj)  # type: ignore

    def unstructure_attrs_asdict(self, obj, *, ignore_empty=True) -> Dict[str, Any]:
        attrs = obj.__class__.__attrs_attrs__
        dispatch = self._unstructure_func.dispatch
        rv = self._dict_factory()
        for a in attrs:
            name = a.name
            v = getattr(obj, name)

            if ignore_empty is True:
                if isinstance(self.MISSING, type(v)):
                    continue

            rv[name] = dispatch(v.__class__)(v)
        return rv


converter: ClassVar[Type[cattr.Converter]] = BaseConverter()


class BaseModelOperations(object):

    def to_xml(self, *, root, ignore_empty=True):
        _body = self.to_dict(ignore_empty=ignore_empty)
        if root:
            _body = {root: _body}
        return xmltodict.unparse(_body, full_document=False)

    def to_dict(cls, *, ignore_empty=True):
        return converter.unstructure_attrs_asdict(cls, ignore_empty=ignore_empty)

    @classmethod
    def from_xml(cls, xml_str: str, root: str = None, *, ignore_extra_args=False):
        _xml = xmltodict.parse(xml_str)
        _body = json.dumps(_xml)
        _body = json.loads(_body)
        if root:
            _body = _body[root]

        return cls.from_dict(_body, ignore_extra_args=ignore_extra_args)

    @classmethod
    def from_dict(cls, d: dict, *, ignore_extra_args=False):
        return converter.structure_attrs_fromdict(d, cls, ignore_extra_args=ignore_extra_args)
