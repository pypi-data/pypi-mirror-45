from dissononce.cipher.cipher import Cipher
from dissononce.exceptions.decrypt import DecryptFailedException

from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from cryptography.exceptions import InvalidTag
import struct


class AESCCMCipher(Cipher):
    def __init__(self, tag_length=16):
        super(AESCCMCipher, self).__init__("AESCCM")
        self._tag_length = tag_length

    def encrypt(self, key, nonce, ad, plaintext):
        return AESCCM(key, tag_length=self._tag_length).encrypt(self.__class__._format_nonce(nonce), plaintext, ad)

    def decrypt(self, key, nonce, ad, ciphertext):
        try:
            return AESCCM(key, tag_length=self._tag_length).decrypt(self.__class__._format_nonce(nonce), ciphertext, ad)
        except InvalidTag:
            raise DecryptFailedException(DecryptFailedException.REASON_INVALID_TAG)

    @staticmethod
    def _format_nonce(n):
        return b'\x00\x00\x00\x00' + struct.pack('>Q', n)
