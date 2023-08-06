import re
import pytest
from typing import AnyStr

from edback.structures.key import Key


def test_key_key_is_immutable(dummy_key: Key):
    with pytest.raises(AttributeError):
        dummy_key.key = 'Error!'


def test_key_iv_is_immutable(dummy_key: Key):
    with pytest.raises(AttributeError):
        dummy_key.iv = 'Error!'


def test_key_serialize_and_deserialize(dummy_key: Key):
    key = Key.deserialize(dummy_key.serialize())
    assert key == dummy_key


def test_key_from_file(dummy_keyfile: AnyStr):
    key = Key.from_file(dummy_keyfile)
    assert key.key == '1449e3b02efa4479feeefed579167140d45e2b5263fc65e6522fc0ac3de4338a'
    assert key.iv == '2234921358b0eb6df9a6ae5824bc9ac6'


def test_key_random():
    key = Key.random()
    assert re.match('^[a-f0-9]{64}$', key.key)
    assert re.match('^[a-f0-9]{32}$', key.iv)
