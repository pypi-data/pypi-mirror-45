from dissononce.cipher.cipher import Cipher
import struct
from Crypto.Cipher import AES


class AESGCMCipher(Cipher):

    def __init__(self):
        super(AESGCMCipher, self).__init__("AESGCM")

    def encrypt(self, key, nonce, ad, plaintext):
        cipher = AES.new(key, AES.MODE_GCM, nonce=self._format_nonce(nonce))
        cipher.update(ad)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return ciphertext + tag

    def decrypt(self, key, nonce, ad, ciphertext):
        cipher = AES.new(key, AES.MODE_GCM, nonce=self._format_nonce(nonce))
        cipher.update(ad)
        return cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])

    @staticmethod
    def _format_nonce(n):
        return b'\x00\x00\x00\x00' + struct.pack('>Q', n)
