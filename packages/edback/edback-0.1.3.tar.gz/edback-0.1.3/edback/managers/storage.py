import os
from typing import AnyStr

from edback.enums.type import StorageType
from edback.managers.resource import ResourceManager
from edback.structures.storage import Storage


class StorageManager(ResourceManager):
    default_resources = {
        'main': {
            'type': 'local',
            'url': os.getenv('HOME'),
            'name': 'main',
            'backups': [],
        }
    }

    resource_type = Storage

    def create(self, name: AnyStr, type: StorageType, url: AnyStr) -> Storage:
        self._check_duplication(name)
        storage = Storage([], type, url)
        self._resources[name] = storage
        return storage
