import unittest

from dissononce.hash.sha256 import SHA256Hash


class SHA256HashTest(unittest.TestCase):
    def setUp(self):
        self.hash = SHA256Hash()

    def test_hash(self):
        expected1 = bytes(bytearray([93, 143, 207, 239, 169, 174, 235, 113, 31, 184, 237, 30, 75, 125, 92, 138, 155, 175, 164, 110,
                          142, 118, 230, 138, 161, 138, 220, 229, 161, 13, 246, 171]))
        expected2 = bytes(bytearray([90, 125, 66, 149, 255, 174, 168, 26, 41, 230, 219, 69, 189, 191, 93, 178, 132, 254, 59, 223,
                           156, 180, 247, 96, 3, 17, 153, 101, 45, 229, 112, 158]))

        hashfn = SHA256Hash()
        data1 = bytes(bytearray(range(0, 33)))
        data2 = bytes(bytearray([1, 2, 3, 4]))
        hash1 = hashfn.hash(data1)
        self.assertEqual(expected1, hash1)
        self.assertEqual(expected2, hashfn.hash(hash1 + data2))
