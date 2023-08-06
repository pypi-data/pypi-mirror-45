from typing import AnyStr


from edback.managers.resource import ResourceManager
from edback.structures.key import Key


class KeyManager(ResourceManager):
    default_resources = dict()
    resource_type = Key

    def create(self, name: AnyStr) -> Key:
        self._check_duplication(name)
        key = Key.random()
        self._resources[name] = key
        return key
