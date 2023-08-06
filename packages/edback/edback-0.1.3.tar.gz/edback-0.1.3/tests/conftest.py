import json
import pathlib
from typing import AnyStr, TextIO

import pytest

from edback.enums.type import StorageType
from edback.managers.backup import BackupManager
from edback.structures.backup import Backup
from edback.structures.key import Key
from edback.structures.storage import Storage


@pytest.fixture
def dummy_file_path(tmp_path: pathlib.Path) -> AnyStr:
    dummy_file = tmp_path / 'dummy_file'
    dummy_file.write_text('Hello World! I love checksum!!')
    dummy_file_path = str(dummy_file)
    return dummy_file_path


@pytest.fixture
def dummy_backup(backup_manager: BackupManager, dummy_file_path: AnyStr, dummy_key: Key) -> Backup:
    backup = backup_manager.create('Backup message', dummy_file_path, [], dummy_key)
    return backup


@pytest.fixture
def dummy_backup_corrupted(dummy_file_path: AnyStr) -> Backup:
    dummy_backup_corrupted = Backup('Backup corrupted', dummy_file_path, dummy_file_path, {'love', 'corrupted'},
                                    '6e6d65d7282003314c38e17bdefd475a', 1555994950.0946581)
    return dummy_backup_corrupted


@pytest.fixture
def dummy_backup_tags(dummy_file_path: AnyStr) -> Backup:
    dummy_backup_tags = Backup('Backup with tags :)', dummy_file_path, '', {'love', 'tags'})
    return dummy_backup_tags


@pytest.fixture
def backup_manager(tmp_path: pathlib.Path) -> BackupManager:
    backup_manager = BackupManager(str(tmp_path))
    return backup_manager


@pytest.fixture
def dummy_storage() -> Storage:
    dummy_storage = Storage([], StorageType.LOCAL, '/tmp/my-storage')
    return dummy_storage


@pytest.fixture
def dummy_key() -> Key:
    key = Key(
        '1449e3b02efa4479feeefed579167140d45e2b5263fc65e6522fc0ac3de4338a',
        '2234921358b0eb6df9a6ae5824bc9ac6')
    return key


@pytest.fixture
def dummy_keyfile_path(dummy_key: Key, tmp_path: pathlib.Path) -> AnyStr:
    content = json.dumps(dummy_key.serialize())

    dummy_keyfile = tmp_path / 'dummy_key_file'
    dummy_keyfile.write_text(content)
    dummy_keyfile_path = str(dummy_keyfile)
    return dummy_keyfile_path


@pytest.fixture
def dummy_keyfile(dummy_keyfile_path: AnyStr) -> TextIO:
    return open(dummy_keyfile_path, 'r')
