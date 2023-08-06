from typing import Any


class DuplicationException(Exception):
    """Exception raised when there were elements duplication"""

    def __init__(self, _duplicated_object: Any):
        self._duplicated_object = _duplicated_object

    @property
    def duplicated_object(self):
        return self._duplicated_object


class NotExistsException(Exception):
    """Exception raised when there weren't elements you wanna find"""


class CorruptedException(Exception):
    """Exception raised when there were elements corrupted
    { 'keys' : [...] } was expected, but there was { 'koss' : [...] }, then it will be raised
    """
