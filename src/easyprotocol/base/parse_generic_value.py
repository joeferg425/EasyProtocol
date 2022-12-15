from __future__ import annotations

from typing import Any, Generic, Iterable, TypeVar

from easyprotocol.base.parse_generic import ParseBase, dataT, endianT

T = TypeVar("T", covariant=True)


class ParseGenericValue(
    ParseBase,
    Generic[T],
):
    def __init__(
        self,
        name: str,
        default: T = None,
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

    def get_value(self) -> T:
        raise NotImplementedError()

    def set_value(self, value: Any) -> None:
        raise NotImplementedError()

    @property
    def value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: T | Iterable[Any] | Any) -> None:
        self.set_value(value)

    @property
    def parent(self) -> ParseBase | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_parent_generic()

    @parent.setter
    def parent(self, value: ParseBase) -> None:
        self._set_parent_generic(value)
