import unittest

from dissononce.processing.impl.cipherstate import CipherState
from dissononce.cipher.aesgcm import AESGCMCipher


class CipherStateTest(unittest.TestCase):
    def setUp(self):
        self.cipherstate = CipherState(AESGCMCipher())
        self.key = bytes(bytearray([175, 166, 245, 84, 218, 17, 230, 108, 187, 247, 207, 150, 101, 249, 81, 31, 28, 227, 60, 132,
                          1, 243, 42, 88, 50, 89, 140, 66, 209, 148, 131, 53]))

    def test_encrypt_with_ad(self):

        expected_ciphertext1 = bytes(bytearray([191, 129, 84, 121, 159, 236, 62, 240, 184, 29, 125, 179, 237, 192, 7, 189, 215,
                                      212, 197, 197, 191, 107, 143, 245]))
        expected_ciphertext2 = bytes(bytearray([224, 247, 48, 37, 200, 167, 11, 97, 168, 223, 107, 63, 218, 3, 166, 180, 241,
                                      21, 244, 56, 146, 207, 132, 141]))

        plaintext = bytes(bytearray([1, 2, 3, 4, 5, 6, 7, 8]))

        self.cipherstate.initialize_key(self.key)

        ciphertext1 = self.cipherstate.encrypt_with_ad(b"", plaintext)
        ciphertext2 = self.cipherstate.encrypt_with_ad(b"", plaintext)

        self.assertEqual(expected_ciphertext1, ciphertext1)
        self.assertEqual(expected_ciphertext2, ciphertext2)

    def test_decrypt_with_ad(self):
        ciphertext1 = bytes(bytearray([191, 129, 84, 121, 159, 236, 62, 240, 184, 29, 125, 179, 237, 192, 7, 189, 215, 212, 197,
                               197, 191, 107, 143, 245]))
        ciphertext2 = bytes(bytearray([224, 247, 48, 37, 200, 167, 11, 97, 168, 223, 107, 63, 218, 3, 166, 180, 241, 21, 244, 56,
                             146, 207, 132, 141]))
        expected_plaintext = bytes(bytearray([1, 2, 3, 4, 5, 6, 7, 8]))

        self.cipherstate.initialize_key(self.key)

        self.assertEqual(expected_plaintext, self.cipherstate.decrypt_with_ad(b"", ciphertext1))
        self.assertEqual(expected_plaintext, self.cipherstate.decrypt_with_ad(b"", ciphertext2))
