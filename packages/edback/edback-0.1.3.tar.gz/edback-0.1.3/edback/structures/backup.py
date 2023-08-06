import time
from typing import Any, AnyStr, Set

from edback.exceptions import CorruptedException
from edback.structures.object import EdbackObject
from edback.utils import checksum, type


class Backup(EdbackObject):

    def __init__(self, _message: AnyStr, _path: AnyStr, _stored_path: AnyStr, _tags: Set[AnyStr] = None,
                 _hash: AnyStr = None,
                 _created_at: float = time.time()):
        """
        __init__#Backup

        :param _message: Backup message to describe how backup is
        :param _path: Path where created, to give hint when user wanna revert
        :param _stored_path: Path where stored
        :param _tags: tags of backup, criterion to filter
        :param _hash: unique value to distinguish from others
        :param _created_at: Created time
        """
        self._message = _message
        self._path = _path
        self._created_at = _created_at
        self._stored_path = _stored_path

        if _hash is None:
            _hash = self._calculate_hash()

        if _tags is None:
            _tags = set()

        self._hash = _hash
        self.tags = _tags

    def _calculate_hash(self) -> AnyStr:
        return checksum.get_checksum(self._stored_path)

    @property
    def message(self) -> AnyStr:
        return self._message

    @property
    def created_at(self) -> float:
        return self._created_at

    @property
    def hash(self) -> AnyStr:
        return self._hash

    @property
    def path(self) -> AnyStr:
        return self._path

    @property
    def is_corrupted(self) -> bool:
        return self.hash != self._calculate_hash()

    @property
    def stored_path(self) -> AnyStr:
        return self._stored_path

    def __str__(self):
        return f"[{self.hash[:6]}] {self.message}"

    def serialize(self) -> dict:
        return {
            'message': self.message,
            'path': self.path,
            'tags': list(self.tags),
            'hash': self.hash,
            'created_at': self.created_at,
            'stored_path': self.stored_path,
        }

    @staticmethod
    def deserialize(data: dict) -> Any:
        is_corrupted = False
        try:
            is_corrupted |= not type.is_string(data['message'])
            is_corrupted |= not type.is_string(data['path'])
            is_corrupted |= not type.is_list_of(data['tags'], str)
            is_corrupted |= not type.is_string(data['hash'])
            is_corrupted |= not type.is_string(data['stored_path'])
            is_corrupted |= not type.is_float(data['created_at'])

            if is_corrupted:
                raise CorruptedException()

            backup = Backup(data['message'], data['path'], data['stored_path'], set(data['tags']), data['hash'],
                            data['created_at'])
            return backup
        except KeyError:
            raise CorruptedException()
