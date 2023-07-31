# flake8:noqa
from __future__ import annotations

import pytest

from easyprotocol.base.value import ValueFieldGeneric


class TestValue:
    def test_value_value_get(self) -> None:
        name = "test"
        f = ValueFieldGeneric[int](name=name)
        with pytest.raises(NotImplementedError):
            f.value

    def test_value_value_set(self) -> None:
        name = "test"
        f = ValueFieldGeneric[int](name=name)
        with pytest.raises(NotImplementedError):
            f.value = 0
