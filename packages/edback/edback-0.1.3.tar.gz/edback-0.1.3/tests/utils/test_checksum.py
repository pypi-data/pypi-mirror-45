from edback.utils import checksum


def test_get_checksum(dummy_file_path):
    hashed_value = '5b2249ba09bba9a1ecedc176a0e84cc7'
    assert checksum.get_checksum(dummy_file_path) == hashed_value
