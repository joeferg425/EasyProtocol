from typing import Any, Sequence, Union

from easyprotocol.base.base_dict_field import BaseDictField
from easyprotocol.base.base_field import BaseParseField, T
from easyprotocol.base.base_list_field import BaseListField

# from easyprotocol.base.parse_generic_field_value_list import ParseGenericFieldValueList
from easyprotocol.base.base_value_field import BaseValueField

fieldGenericT = Union[
    BaseParseField,
    BaseValueField[T],
    BaseDictField[T],
    BaseListField[T],
    # ParseGenericFieldValueList[T],
]
collectionGenericT = Union[
    Sequence[fieldGenericT[T]],
    "dict[str, fieldGenericT[T]]",
    Any,
]
valueGenericT = Union[
    Sequence[T],
    "dict[str, T]",
    Any,
]
