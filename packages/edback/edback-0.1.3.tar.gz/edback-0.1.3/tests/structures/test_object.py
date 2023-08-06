import pytest

from edback.structures.object import EdbackObject

edback_object = EdbackObject()


def test_edback_object_serialize_not_implemented():
    with pytest.raises(NotImplementedError):
        edback_object.serialize()


def test_edback_object_deserialize_not_implemented():
    with pytest.raises(NotImplementedError):
        EdbackObject.deserialize({})