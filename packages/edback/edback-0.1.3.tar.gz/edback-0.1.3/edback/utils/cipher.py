import base64

from Crypto.Cipher import AES

from edback.structures.key import Key


class AESCipher:
    def __init__(self, _key: Key):
        self._key = bytes.fromhex(_key.key)
        self._iv = bytes.fromhex(_key.iv)

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self._key, AES.MODE_CBC, self._iv)
        return cipher.encrypt(raw)

    def decrypt(self, enc):
        cipher = AES.new(self._key, AES.MODE_CBC, self._iv)
        return self._unpad(cipher.decrypt(enc))

    def _pad(self, s):
        block_size = AES.block_size
        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size).encode()

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
