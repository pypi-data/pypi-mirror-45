import json
import os
from typing import AnyStr, Dict, Union

from edback.exceptions import DuplicationException, NotExistsException, CorruptedException
from edback.managers.base import Manager
from edback.structures.object import EdbackObject


class ResourceManager(Manager):
    default_resources = {'name': EdbackObject()}
    resource_name = None
    resource_type = EdbackObject

    def remove(self, name: AnyStr):
        if name not in self._resources.keys():
            raise NotExistsException(f"The key '{name}' doesn't exist")

        del self._resources[name]

    def create(self, *args) -> EdbackObject:
        raise NotImplementedError()

    def get(self, name: AnyStr, default=None) -> EdbackObject:
        try:
            return self._resources.get(name, default)
        except KeyError:
            return default

    def add(self, name: AnyStr, resource: EdbackObject):
        if name in self._resources:
            raise DuplicationException(name)

        self._resources[name] = resource

    def _initialize_variables(self):
        if self.resource_name is None:
            self.resource_name = self.resource_type.__name__.lower() + 's'

        self._resources: Dict[AnyStr, EdbackObject] = dict()
        self._state_path = os.path.join(self.base_path, f'{self.resource_name}.json')
        self._resources_path = os.path.join(self.base_path, f'{self.resource_name}')

    def _exists_or_create_directory(self):
        os.makedirs(self._resources_path, exist_ok=True)

    def _check_duplication(self, name: AnyStr):
        if name in self._resources:
            raise DuplicationException(name)

    def _load(self):
        state_data = self._load_state_file()
        if self.resource_name not in state_data:
            raise CorruptedException("There was no element named '%s'" % self.resource_name)

        resources = state_data[self.resource_name]
        for name, resource in resources.items():
            self._resources[name] = self.resource_type.deserialize(resource)

    def _load_state_file(self) -> Dict[AnyStr, Dict[AnyStr, EdbackObject]]:
        try:
            with open(self._state_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {self.resource_name: self.default_resources}

    def _save(self):
        self._save_state_file()

    def _save_state_file(self):
        def serialize(t: Union[AnyStr, EdbackObject]):
            return t[0], t[1].serialize()

        data = {
            self.resource_name: dict(map(serialize, self._resources.items()))
        }

        self._write_state_file(json.dumps(data))

    def _write_state_file(self, content: AnyStr):
        with open(self._state_path, 'w') as f:
            f.write(content)

    def __getattr__(self, item: AnyStr):
        if item == self.resource_name:
            return self._resources
