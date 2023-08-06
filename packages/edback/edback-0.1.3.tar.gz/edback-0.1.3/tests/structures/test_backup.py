import re
import pytest

from edback.structures.backup import Backup


def test_backup_calculate_hash(dummy_backup: Backup):
    assert re.match('^[a-f0-9]$', dummy_backup.hash) is None


def test_backup_get_hash(dummy_backup_corrupted: Backup):
    hashed_value = '5b2249ba09bba9a1ecedc176a0e84cc7'
    assert dummy_backup_corrupted.hash != hashed_value


def test_backup_is_corrupted(dummy_backup_corrupted: Backup):
    assert dummy_backup_corrupted.is_corrupted


def test_backup_tags_no_duplication(dummy_backup: Backup):
    dummy_backup.tags.add('needs')
    dummy_backup.tags.add('needs')
    assert dummy_backup.tags == set(('needs',))


def test_backup_tags_empty_set(dummy_backup: Backup):
    assert dummy_backup.tags == set()


def test_backup_hash_is_immutable(dummy_backup: Backup):
    with pytest.raises(AttributeError):
        dummy_backup.hash = 'Error!'


def test_backup_message_is_immutable(dummy_backup: Backup):
    with pytest.raises(AttributeError):
        dummy_backup.message = 'Error!'


def test_backup_created_at_is_immutable(dummy_backup: Backup):
    with pytest.raises(AttributeError):
        dummy_backup.created_at = 'Error!'


def test_backup_path_is_immutable(dummy_backup: Backup):
    with pytest.raises(AttributeError):
        dummy_backup.path = 'Error!'


def test_backup_serialize_and_deserialize(dummy_backup_corrupted: Backup):
    backup = Backup.deserialize(dummy_backup_corrupted.serialize())
    assert backup.hash == dummy_backup_corrupted.hash
    assert backup.created_at == dummy_backup_corrupted.created_at
    assert backup.path == dummy_backup_corrupted.path
    assert backup.message == dummy_backup_corrupted.message
    assert backup.tags == dummy_backup_corrupted.tags
