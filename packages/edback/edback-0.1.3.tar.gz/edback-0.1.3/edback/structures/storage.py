from typing import List, AnyStr, Any

from edback.enums.type import StorageType
from edback.structures.backup import Backup
from edback.structures.object import EdbackObject


class Storage(EdbackObject):
    def __init__(self, _backups: List[Backup], _type: StorageType, _url: AnyStr):
        self._backups = _backups
        self._type = _type
        self._url = _url

    def clean(self):
        raise NotImplementedError()

    def initialize(self):
        raise NotImplementedError()

    @property
    def is_initialized(self) -> bool:
        raise NotImplementedError()

    @property
    def url(self) -> AnyStr:
        return self._url

    @property
    def backups(self):
        return self._backups

    @property
    def type(self):
        return self._type

    def _process_append_backup(self, backup: Backup):
        raise NotImplementedError()

    def append(self, backup: Backup):
        self._process_append_backup(backup)
        self._backups.append(backup)

    def serialize(self) -> dict:
        return {
            'backups': [backup.serialize() for backup in self.backups],
            'type': self.type.value,
            'url': self.url,
        }

    @staticmethod
    def deserialize(data: dict) -> Any:
        backups = [Backup.deserialize(backup) for backup in data['backups']]
        storage = Storage(backups, StorageType(data['type']), data['url'])
        return storage
