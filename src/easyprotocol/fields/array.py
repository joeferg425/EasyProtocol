from __future__ import annotations

from collections import OrderedDict
from typing import Any, Generic, Sequence, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_field_dict import parseGenericT
from easyprotocol.base.parse_field_list import ParseFieldListGeneric
from easyprotocol.base.parse_generic import ParseBase
from easyprotocol.base.parse_generic_dict import K, ParseGenericDict
from easyprotocol.base.parse_generic_list import ParseGenericList
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.parse_value_list import ParseValueListGeneric, T
from easyprotocol.base.utils import dataT, input_to_bytes
from easyprotocol.fields.unsigned_int import UIntFieldGeneric


class ParseArrayFieldGeneric(
    ParseFieldListGeneric[T, K],
    Generic[T, K],
):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseGenericValue[T]],
        array_item_default: T,
        default: Sequence[T] | Sequence[ParseGenericValue[T]] = list(),
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        self._count = count
        self._array_item_class = array_item_class
        self._array_item_default = array_item_default
        super().__init__(
            name=name,
            data=None,
            string_format=string_format,
        )
        self.create_default(default=default)
        if data is not None:
            self.parse(data=data)

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, UIntFieldGeneric):
            count = self._count.value
        else:
            count = self._count
        if count is not None:
            for i in range(count):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=self._array_item_default,
                )
                bit_data = f.parse(data=bit_data)
                self._children[f.name] = f
        return bit_data

    def create_default(self, default: Sequence[T] | Sequence[ParseGenericValue[T]]) -> None:
        for i, item in enumerate(default):
            if isinstance(item, ParseGenericValue):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(ParseGenericValue[T], item).value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(T, item),
                )
            self._children[f.name] = f

    def set_value(
        self,
        value: Sequence[parseGenericT[K, T] | Any]
        | OrderedDict[
            str,
            parseGenericT[K, T] | Any,
        ],
    ) -> None:
        if value is not None:
            if isinstance(value, (Sequence)):
                for index in range(len(value)):
                    item = value[index]
                    if isinstance(item, ParseBase):
                        if index < len(self.children):
                            self[index] = item
                            item._set_parent_generic(self)
                        else:
                            item = self._array_item_class(
                                name=f"#{index}",
                                default=item,
                            )
                            item._set_parent_generic(self)
                            self._children[item.name] = item
                    else:
                        self[index].value = item
            else:
                keys = list(value.keys())
                for index in range(len(keys)):
                    key = keys[index]
                    item = value[key]
                    if isinstance(item, ParseBase):
                        if index < len(self.children):
                            self[index] = item
                            item._set_parent_generic(self)
                        else:
                            item = self._array_item_class(
                                name=f"#{index}",
                                default=item,
                            )
                            item._set_parent_generic(self)
                            self._children[item.name] = item
                    else:
                        self[index].value = item


class ParseArrayField(
    ParseArrayFieldGeneric[T, str],
    Generic[T],
):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseGenericValue[T]],
        array_item_default: T,
        default: Sequence[ParseGenericValue[T]] | Sequence[T] = list(),
        string_format: str = "{}",
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=name,
            count=count,
            array_item_class=array_item_class,
            array_item_default=array_item_default,
            data=None,
            string_format=string_format,
        )
        self.create_default(default=default)
        if data is not None:
            self.parse(data=data)

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, UIntFieldGeneric):
            count = self._count.value
        else:
            count = self._count
        if count is not None:
            for i in range(count):
                f = self._array_item_class(name=f"#{i}", default=self._array_item_default)
                bit_data = f.parse(data=bit_data)
                self._children[f.name] = f
        return bit_data

    def create_default(self, default: Sequence[T] | Sequence[ParseGenericValue[T]]) -> None:
        for i, item in enumerate(default):
            if isinstance(item, ParseBase):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(ParseGenericValue[T], item).value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(T, item),
                )
            self._children[f.name] = f


class ParseValueArrayFieldGeneric(
    ParseValueListGeneric[K, T],
    Generic[T, K],
):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseGenericValue[T]],
        array_item_default: T,
        default: Sequence[T] | Sequence[ParseGenericValue[T]] = list(),
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        self._count = count
        self._array_item_class = array_item_class
        self._array_item_default = array_item_default
        super().__init__(
            name=name,
            data=None,
            string_format=string_format,
        )
        self.create_default(default=default)
        if data is not None:
            self.parse(data=data)

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, UIntFieldGeneric):
            count = self._count.value
        else:
            count = self._count
        if count is not None:
            for i in range(count):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=self._array_item_default,
                )
                bit_data = f.parse(data=bit_data)
                self._children[f.name] = f
        return bit_data

    def create_default(self, default: Sequence[T] | Sequence[ParseGenericValue[T]]) -> None:
        for i, item in enumerate(default):
            if isinstance(item, ParseGenericValue):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(ParseGenericValue[T], item).value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(T, item),
                )
            self._children[f.name] = f

    def set_value(
        self,
        value: Sequence[parseGenericT[K, T] | Any]
        | OrderedDict[
            str,
            parseGenericT[K, T] | Any,
        ],
    ) -> None:
        if value is not None:
            if isinstance(value, (Sequence)):
                for index in range(len(value)):
                    item = value[index]
                    if isinstance(item, ParseGenericValue):
                        if index < len(self.children):
                            self[index] = cast("ParseGenericValue[T]", item)
                            item._set_parent_generic(self)
                        else:
                            item = self._array_item_class(
                                name=f"#{index}",
                                default=item,
                            )
                            item._set_parent_generic(self)
                            self._children[item.name] = item
                    else:
                        self[index] = cast("ParseGenericValue[T]", item)
            else:
                keys = list(value.keys())
                for index in range(len(keys)):
                    key = keys[index]
                    item = value[key]
                    if isinstance(item, ParseGenericValue):
                        if index < len(self.children):
                            self[index] = cast("ParseGenericValue[T]", item)
                            item._set_parent_generic(self)
                        else:
                            item = self._array_item_class(
                                name=f"#{index}",
                                default=item,
                            )
                            item._set_parent_generic(self)
                            self._children[item.name] = item
                    else:
                        self[index] = cast("ParseGenericValue[T]", item)

    def append(self, value: ParseGenericValue[T]) -> None:
        self.children[value.name] = value


class ParseValueArrayField(ParseValueArrayFieldGeneric[T, str]):
    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseGenericValue[T]],
        array_item_default: T,
        default: Sequence[T] | Sequence[ParseGenericValue[T]] = list(),
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        super().__init__(
            name,
            count,
            array_item_class,
            array_item_default,
            default,
            data,
            string_format,
        )
