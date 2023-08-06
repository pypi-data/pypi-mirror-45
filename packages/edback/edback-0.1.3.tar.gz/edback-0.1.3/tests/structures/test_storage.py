import pytest

from edback.structures.storage import Storage
from edback.structures.backup import Backup


def test_storage_clean_not_implemented(dummy_storage: Storage):
    with pytest.raises(NotImplementedError):
        dummy_storage.clean()


def test_storage_is_initialized_not_implemented(dummy_storage: Storage):
    with pytest.raises(NotImplementedError):
        dummy_storage.is_initialized


def test_storage_initialize_not_implemented(dummy_storage: Storage):
    with pytest.raises(NotImplementedError):
        dummy_storage.initialize()


def test_storage_url_setter(dummy_storage: Storage):
    with pytest.raises(AttributeError):
        dummy_storage.url = "/new/url"


def test_storage_backup_append(dummy_storage: Storage, dummy_backup: Backup):
    with pytest.raises(NotImplementedError):
        dummy_storage.append(dummy_backup)


def test_storage_serialize_and_deserialize(dummy_storage: Storage):
    storage = Storage.deserialize(dummy_storage.serialize())
    assert storage.type == dummy_storage.type
    assert storage.url == dummy_storage.url
    assert storage.backups == dummy_storage.backups
