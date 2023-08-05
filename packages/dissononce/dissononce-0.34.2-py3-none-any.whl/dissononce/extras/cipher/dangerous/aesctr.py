from dissononce.cipher import cipher

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct


class AESCTRCipher(cipher.Cipher):
    def __init__(self):
        super(AESCTRCipher, self).__init__("AESCTR")

    def encrypt(self, key, nonce, ad, plaintext):
        cipher = Cipher(algorithms.AES(key), modes.CTR(self._format_nonce(nonce)), backend=default_backend()).encryptor()
        cipher.update(self._format_nonce(nonce))
        cipher.update(ad)
        return cipher.update(plaintext)

    def decrypt(self, key, nonce, ad, ciphertext):
        cipher = Cipher(algorithms.AES(key), modes.CTR(self._format_nonce(nonce)), backend=default_backend()).decryptor()
        cipher.update(self._format_nonce(nonce))
        cipher.update(ad)
        return cipher.update(ciphertext)

    @staticmethod
    def _format_nonce(n):
        return b'\x00\x00\x00\x00\x00\x00\x00\x00' + struct.pack('>Q', n)
