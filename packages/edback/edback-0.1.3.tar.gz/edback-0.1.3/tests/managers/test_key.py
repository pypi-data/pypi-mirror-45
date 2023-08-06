import pytest
import pathlib

from edback.managers.key import KeyManager


@pytest.fixture
def manager(tmp_path: pathlib.Path) -> KeyManager:
    manager = KeyManager(str(tmp_path))
    return manager


def test_key_manager_save_and_load(tmp_path: pathlib.Path):
    def create_and_destroy():
        manager = KeyManager(str(tmp_path))
        manager.create("my-key")

    create_and_destroy()

    new_manager = KeyManager(str(tmp_path))

    assert new_manager.keys.get('my-key', None) is not None


def test_key_manager_keys(manager: KeyManager):
    manager.create('my-key')
    assert manager.keys.get('my-key', None) is not None


def test_key_manager_create_and_remove(manager: KeyManager):
    manager.create('my-key')
    assert manager.keys.get('my-key', None) is not None
    manager.remove('my-key')
    assert manager.keys.get('my-key', None) is None
