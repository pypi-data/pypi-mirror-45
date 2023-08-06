import pytest
import pathlib

from edback.enums.type import StorageType
from edback.managers.storage import StorageManager


@pytest.fixture
def manager(tmp_path: pathlib.Path) -> StorageManager:
    manager = StorageManager(str(tmp_path))
    return manager


def test_storage_manager_save_and_load(tmp_path: pathlib.Path):
    def create_and_destroy():
        manager = StorageManager(str(tmp_path))
        manager.create("my-storage", StorageType.LOCAL, str(tmp_path))

    create_and_destroy()

    new_manager = StorageManager(str(tmp_path))

    assert new_manager.storages.get('my-storage', None) is not None


def test_storage_manager(manager: StorageManager):
    manager.create('my-storage', StorageType.LOCAL, '/tmp/endpoint')
    assert manager.storages.get('my-storage', None) is not None


def test_storage_manager_create_and_remove(manager: StorageManager):
    manager.create('my-storage', StorageType.LOCAL, '/tmp/endpoint')
    assert manager.storages.get('my-storage', None) is not None
    manager.remove('my-storage')
    assert manager.storages.get('my-storage', None) is None
