import pytest

from edback.managers.base import Manager


def test_manager_not_implemented():
    with pytest.raises(NotImplementedError):
        Manager()
