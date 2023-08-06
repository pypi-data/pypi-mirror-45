from edback.utils import type


def test_type_is_string_false():
    assert not type.is_string(0)
    assert not type.is_string(1.1)
    assert not type.is_string([])


def test_type_is_string_true():
    assert type.is_string('')


def test_type_is_float_false():
    assert not type.is_float('')
    assert not type.is_float([])
    assert not type.is_float(1)


def test_type_is_float_true():
    assert type.is_float(1.1)


def test_type_is_list_false():
    assert not type.is_list('')
    assert not type.is_list(1.1)
    assert not type.is_list(1)


def test_type_is_list_true():
    assert type.is_list([])


def test_type_is_list_of_true():
    assert type.is_list_of([1, 2, 3], int)
    assert type.is_list_of(['', '', ''], str)
