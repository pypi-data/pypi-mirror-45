from typing import AnyStr

import pathlib

from edback.managers.backup import BackupManager
from edback.structures.backup import Backup
from edback.structures.key import Key


def test_backup_manager_save_and_load(tmp_path: pathlib.Path, dummy_file_path: AnyStr, dummy_key: Key):
    def create_and_destroy() -> Backup:
        manager = BackupManager(str(tmp_path))
        return manager.create("my-backup", dummy_file_path, [], dummy_key)

    backup = create_and_destroy()

    new_manager = BackupManager(str(tmp_path))

    assert new_manager.get(backup.hash, None) is not None


def test_backup_manager_keys(backup_manager: BackupManager, dummy_file_path: AnyStr, dummy_key: Key):
    backup = backup_manager.create("my-backup", str(dummy_file_path), [], dummy_key)
    assert backup_manager.get(backup.hash, None) is not None


def test_backup_manager_create_and_remove(backup_manager: BackupManager, dummy_file_path: AnyStr, dummy_key: Key):
    backup = backup_manager.create("my-backup", dummy_file_path, [], dummy_key)
    assert backup_manager.get(backup.hash, None) is not None
    backup_manager.remove(backup.hash)
    assert backup_manager.get(backup.hash, None) is None


def test_backup_directory_backup(backup_manager: BackupManager, tmp_path: pathlib.Path, dummy_key: Key):
    backup = backup_manager.create("my-backup", str(tmp_path), [], dummy_key)
    assert backup_manager.get(backup.hash, None) is not None
