import re
import json
from hashlib import sha256
from typing import Any, AnyStr, TextIO

from Crypto import Random

from edback.exceptions import CorruptedException
from edback.structures.object import EdbackObject


class Key(EdbackObject):
    def __init__(self, _key: AnyStr, _iv: AnyStr):
        self._key = _key
        self._iv = _iv

    @property
    def key(self) -> AnyStr:
        return self._key

    @property
    def iv(self) -> AnyStr:
        return self._iv

    @staticmethod
    def from_path(filename: AnyStr) -> Any:
        with open(filename) as f:
            data = json.load(f)

        return Key.deserialize(data)

    @staticmethod
    def from_file(file: TextIO):
        data = json.load(file)
        return Key.deserialize(data)

    @staticmethod
    def deserialize(data: dict) -> Any:
        try:
            if not re.match('^[a-z0-9]{64}$', data['key'])\
                    or not re.match('^[a-z0-9]{32}$', data['iv']):
                raise CorruptedException()

            return Key(data['key'], data['iv'])
        except KeyError:
            raise CorruptedException()

    def __eq__(self, other):
        return other.iv == self.iv and other.key == self.key

    def serialize(self) -> dict:
        return {
            'key': self.key,
            'iv': self.iv,
        }

    @staticmethod
    def random() -> Any:
        random = Random.new()
        key = sha256(random.read(32)).digest().hex()
        iv = random.read(16).hex()
        return Key(key, iv)
