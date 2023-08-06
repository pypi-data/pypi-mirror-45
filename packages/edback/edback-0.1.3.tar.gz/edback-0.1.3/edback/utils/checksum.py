import hashlib
import sys
from typing import AnyStr


def get_checksum(filename: AnyStr) -> AnyStr:
    content = _get_file_content(filename)
    return hashlib.md5(content).hexdigest()


def _get_file_content(filename: AnyStr) -> bytes:
    with open(filename, 'rb') as f:
        return f.read()
