import os
import shutil
import zipfile
from typing import AnyStr, List, Set, Tuple

from edback.exceptions import NotExistsException, CorruptedException
from edback.managers.resource import ResourceManager
from edback.structures.backup import Backup
from edback.structures.key import Key
from edback.utils import checksum
from edback.utils.cipher import AESCipher


class BackupManager(ResourceManager):
    default_resources = dict()
    resource_type = Backup

    def get(self, name: AnyStr, default=None) -> Backup:
        hashes = self.backups.keys()
        filtered_hashes = list(filter(lambda x: x.startswith(name), hashes))

        if len(filtered_hashes) == 1:
            return self.backups[filtered_hashes[0]]
        else:
            return default

    def create(self, message: AnyStr, path: AnyStr, tags: List[AnyStr], key: Key) -> Backup:
        backup = self._backup(message, path, set(tags), key)

        self._check_duplication(backup.hash)
        self._resources[backup.hash] = backup
        return backup

    def revert(self, hash: AnyStr, dest: AnyStr, key: Key):
        backup = self.get(hash)

        os.makedirs(dest, exist_ok=True)
        temporary_directory = self._exists_or_create_temporary_directory()
        decrypted_zip_path = os.path.join(temporary_directory, 'decrypted.zip')

        self._decrypt_file(key, backup.stored_path, decrypted_zip_path)
        self._extract_to(decrypted_zip_path, dest)

        os.remove(decrypted_zip_path)

    def _extract_to(self, src: AnyStr, dest: AnyStr):
        zip_ref = zipfile.ZipFile(src, 'r')
        zip_ref.extractall(dest)
        zip_ref.close()

    def _backup(self, message: AnyStr, path: AnyStr, tags: Set[AnyStr], key: Key) -> Backup:
        self._exists_or_create_directory()

        if not os.path.exists(path):
            raise NotExistsException()

        if os.path.isdir(path):
            zip_path = self._compress_directory(path)
        else:
            zip_path = self._compress_file(path)

        enc_zip_path = self._encrypt_file(key, zip_path)
        hash_of_backup = checksum.get_checksum(enc_zip_path)

        backup_path = os.path.join(self._resources_path, hash_of_backup)
        shutil.move(enc_zip_path, backup_path)

        return Backup(message, path, backup_path, tags, hash_of_backup)

    def _encrypt_file(self, key: Key, src: AnyStr, dest: AnyStr = None) -> AnyStr:
        if dest is None:
            dest = src + '.enc'

        with open(src, 'rb') as f:
            data = f.read()

        enc = AESCipher(key).encrypt(data)

        with open(dest, 'wb') as f:
            f.write(enc)

        return dest

    def _decrypt_file(self, key: Key, src: AnyStr, dest: AnyStr):
        with open(src, 'rb') as f:
            enc = f.read()

        content = AESCipher(key).decrypt(enc)

        if content[:4] != b'\x50\x4b\x03\x04':
            raise CorruptedException()

        with open(dest, 'wb') as f:
            f.write(content)

    def _compress_file(self, path: AnyStr) -> AnyStr:
        temporary_zip_path, temporary_zip = self._create_temporary_zipfile()
        temporary_zip.write(path)
        temporary_zip.close()

        return temporary_zip_path

    def _compress_directory(self, path: AnyStr) -> AnyStr:
        temporary_zip_path, temporary_zip = self._create_temporary_zipfile()
        for directory, subdirectories, files in os.walk(path):
            for file in files:
                temporary_zip.write(os.path.join(directory, file),
                                  os.path.relpath(os.path.join(directory, file), path),
                                  compress_type=zipfile.ZIP_DEFLATED)
        temporary_zip.close()

        return temporary_zip_path

    def _exists_or_create_temporary_directory(self) -> AnyStr:
        temporary_directory = '/tmp/.edback_temporary/'
        os.makedirs(temporary_directory, exist_ok=True)
        return temporary_directory

    def _create_temporary_zipfile(self) -> Tuple[AnyStr, zipfile.ZipFile]:
        temporary_directory = self._exists_or_create_temporary_directory()
        temporary_zip_path = os.path.join(temporary_directory, 'compressed.zip')
        temporary_zip = zipfile.ZipFile(temporary_zip_path, 'w', zipfile.ZIP_DEFLATED)
        return temporary_zip_path, temporary_zip
