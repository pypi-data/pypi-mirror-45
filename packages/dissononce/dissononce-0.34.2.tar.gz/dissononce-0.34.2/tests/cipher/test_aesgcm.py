import unittest

from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.dh.x25519.public import PublicKey


class AESGCMCipherTest(unittest.TestCase):
    def setUp(self):
        self.key = PublicKey(bytes(bytearray([190, 9, 95, 224, 225, 206, 108, 98, 214, 155, 99, 25, 148, 232, 242, 134, 169,
                                        54, 131, 72, 157, 163, 88, 247, 158, 91, 81, 117, 79, 142, 220, 65])))
        self.plaintext = b"00000000000000000000000000000000"
        self.ad = b"hello"
        self.ciphertext = bytes(bytearray([113, 62, 52, 230, 198, 144, 211, 132, 219, 41, 17, 89, 25, 12, 111, 76, 52, 87,
                                     179, 11, 231, 79, 183, 113, 253, 64, 180, 116, 93, 243, 222, 232, 239, 153, 42,
                                     172, 29, 255, 255, 15, 121, 191, 51, 73, 86, 174, 86, 17]))
        self.cipher = AESGCMCipher()

    def test_encrypt_with_ad(self):
        ciphertext = self.cipher.encrypt(self.key.data, 0, self.ad, self.plaintext)
        self.assertEqual(self.ciphertext, ciphertext)

    def test_decrypt_with_ad(self):
        plaintext = self.cipher.decrypt(self.key.data, 0, self.ad, self.ciphertext)
        self.assertEqual(self.plaintext, plaintext)
