"""The base parsing object for handling parsing in a convenient (to modify) package."""
from __future__ import annotations

from typing import Any, Literal, Sequence, SupportsBytes, TypeVar, Union

from bitarray import bitarray

from easyprotocol.base.utils import DEFAULT_ENDIANNESS, dataT, endianT, hex

UNDEFINED = "?UNDEFINED?"

T = TypeVar("T")

defaultT = Union[Any, "Sequence[Any]", "Sequence[BaseField]", "dict[str, Any]", "dict[str, BaseField]"]
fieldsT = Union["BaseField", "Sequence[BaseField]", "dict[str, BaseField]"]


class BaseField(SupportsBytes):
    """The base parsing object for handling parsing in a convenient (to modify) package."""

    def __init__(
        self,
        name: str,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        default: defaultT | None = None,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
            default: unused
        """
        self._name: str = ""
        self._endian: endianT = endian
        self._bits: bitarray = bitarray(endian="little")
        self._bit_count: int = bit_count
        self._name = name
        self._initialized = False
        self._parent: BaseField | None = None
        self._children: dict[str, BaseField] = dict()
        if string_format is None:
            self._string_format = "{}"
        else:
            self._string_format = string_format
        if default is not None:
            self.value = default
        if data is not None:
            self.parse(data=data)

    def parse(self, data: dataT) -> bitarray:
        """Parse the passed bits or bytes into meaningful data.

        Args:
            data: bits or bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        raise NotImplementedError()

    def get_name(self) -> str:
        """Get the name of this field.

        Returns:
            the name
        """
        return self._name

    def set_name(self, name: str) -> None:
        """Set the name of this field.

        Args:
            name: the new name of this field
        """
        self._name = name

    def get_bits_lsb(self) -> bitarray:
        """Get the bits of this field in least-significant-bit first format.

        Returns:
            lsb bits
        """
        return self._bits

    def get_bits_msb(self) -> bitarray:
        """Get the bits of this field in most-significant-bit first format.

        Returns:
            msb bits
        """
        b = self.get_bits_lsb().tobytes()
        bits = bitarray(endian="big")
        bits.frombytes(b)
        if self._bit_count != -1:
            return bits[-self._bit_count :]
        else:
            return bits

    def set_bits_lsb(self, bits: bitarray) -> None:
        """Set the bits of this field in least-significant-bit first format.

        Args:
            bits: lsb bits

        Raises:
            NotImplementedError: until you override it in a sub-class
        """
        raise NotImplementedError()

    def get_parent(self) -> BaseField | None:
        """Get parent field.

        Returns:
            parent field
        """
        return self._parent

    def set_parent(self, parent: BaseField | None) -> None:
        """Set parent field.

        Args:
            parent: parent field object
        """
        self._parent = parent

    def get_children(self) -> dict[str, BaseField]:
        """Get the dictionary of child fields.

        Returns:
            dictionary of children
        """
        return self._children

    def set_children(
        self,
        children: defaultT,
    ) -> None:
        """Assign children to this field.

        Args:
            children: dictionary of children

        Raises:
            TypeError: if children are incompatible with this parent
        """
        self._children.clear()
        if isinstance(children, dict):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value.set_parent(self)
        elif isinstance(children, Sequence):
            for value in children:
                self._children[value._name] = value
                value.set_parent(self)
        else:
            raise TypeError(f"children: {children}")

    def get_value_as_string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return UNDEFINED

    def get_value_as_bytes(self) -> bytes:
        """Get the bytes that make up this field.

        If there are not enough bits, the last byte is padded with zeros.

        Returns:
            field bytes
        """
        return self.__bytes__()

    def get_value_as_hex_string(self) -> str:
        """Get the hexadecimal value of this field.

        Returns:
            the hexadecimal value of this field
        """
        return hex(self.get_value_as_bytes())

    @property
    def name(self) -> str:
        """Get the name of the field.

        Returns:
            the name of the field
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def bits_lsb(self) -> bitarray:
        """Get the bit value of the field.

        Returns:
            the bit value of the field
        """
        return self.get_bits_lsb()

    @bits_lsb.setter
    def bits_lsb(self, bits: bitarray) -> None:
        self.set_bits_lsb(bits)

    @property
    def bits(self) -> bitarray:
        """Get the bits of this field in most-significant-bit first format.

        Returns:
            msb bits
        """
        return self.get_bits_msb()

    @property
    def bits_str(self) -> str:
        """Get the bit string of this field in most-significant-bit first format.

        Returns:
            msb bit string
        """
        return f"{self.bits.to01()}:<b"

    @property
    def bits_str_lsb(self) -> str:
        """Get the bit string of this field in least-significant-bit first format.

        Returns:
            lsb bit string
        """
        return f"b>:{self.bits_lsb.to01()}"

    @property
    def string_format(self) -> str:
        """Get the format string of the field.

        Returns:
            the format string of the field
        """
        return self._string_format

    @string_format.setter
    def string_format(self, fmt: str) -> None:
        self._string_format = fmt

    @property
    def endian(self) -> Literal["little", "big"]:
        """Get the byte endianness value of this object.

        Returns:
            the byte endianness value of this object
        """
        return self._endian

    @property
    def value_as_bytes(self) -> bytes:
        """Get the byte value of this object.

        Returns:
            the byte value of this object
        """
        return self.__bytes__()

    @property
    def chain(self) -> str:
        """Create a dot-delimited string representing field hierarchy.

        Returns:
            a string in the format "grandparent.parent.child"
        """
        s = ""
        if self._parent is not None:
            s = self._parent.chain
        if s:
            return f"{s}.{self.name}"
        else:
            return self.name

    @property
    def value_as_string(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.get_value_as_string()

    @property
    def value_as_hex_string(self) -> str:
        """Get the hexadecimal value of this field.

        Returns:
            the hexadecimal value of this field
        """
        return self.get_value_as_hex_string()

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self.get_bits_lsb().tobytes()

    def __str__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"{self._name}: {self.value_as_string}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    @property
    def value(self) -> Any:
        """Get the parsed value of the field.

        Raises:
            NotImplementedError: until implemented in a non-base field
        """
        raise NotImplementedError()

    @value.setter
    def value(
        self,
        value: Any,
    ) -> None:
        raise NotImplementedError()

    @property
    def parent(self) -> BaseField | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_parent()

    @parent.setter
    def parent(
        self,
        value: BaseField,
    ) -> None:
        self.set_parent(value)

    @property
    def children(self) -> dict[str, BaseField]:
        """Get the dictionary of child fields.

        Returns:
            the child field dictionary
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: dict[str, Any] | Sequence[Any] | dict[str, BaseField] | Sequence[BaseField] | None,
    ) -> None:
        self.set_children(children=children)
