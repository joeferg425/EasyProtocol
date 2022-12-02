from __future__ import annotations

from typing import Any, Generic, TypeVar

from easyprotocol.base.parse_generic import ParseGeneric, T, dataT, endianT

_T = TypeVar("_T")


class ParseGenericValue(
    ParseGeneric[_T],
    Generic[_T],
):
    def __init__(
        self,
        name: str,
        default: _T = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = ...,
    ) -> None:
        super().__init__(
            name,
            data,
            bit_count,
            string_format,
            endian,
        )
        if data is None and default is not None:
            self.value = default

    def get_value(self) -> _T:
        raise NotImplementedError()

    def set_value(self, value: _T) -> None:
        raise NotImplementedError()

    @property
    def value(self) -> _T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: _T) -> None:
        self.set_value(value)

    @property
    def parent(self) -> ParseGeneric[Any] | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_parent_generic()

    @parent.setter
    def parent(self, value: ParseGeneric[Any]) -> None:
        self._set_parent_generic(value)
