from __future__ import annotations

from collections import OrderedDict
from typing import Any, TypeVar

from easyprotocol.base.parse_generic import ParseGeneric, dataT, endianT

T = TypeVar("T", bound=Any)


class ParseValueGeneric(ParseGeneric[T]):
    def __init__(
        self,
        name: str,
        default: T | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = ...,
        parent: ParseGeneric[Any] | None = None,
        children: OrderedDict[str, "ParseGeneric[Any]"]
        | dict[str, "ParseGeneric[Any]"]
        | list["ParseGeneric[Any]"]
        | None = None,
    ) -> None:
        super().__init__(
            name,
            data,
            bit_count,
            string_format,
            endian,
            parent,
            children,
        )
        if data is None and default is not None:
            self.value = default

    def get_value(self) -> T:
        raise NotImplementedError()

    def set_value(self, value: T) -> None:
        raise NotImplementedError()

    @property
    def value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: T) -> None:
        self.set_value(value)

    @property
    def parent(self) -> ParseGeneric[Any] | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_parent_generic()

    @parent.setter
    def parent(self, value: ParseGeneric[Any] | None) -> None:
        self._set_parent_generic(value)
