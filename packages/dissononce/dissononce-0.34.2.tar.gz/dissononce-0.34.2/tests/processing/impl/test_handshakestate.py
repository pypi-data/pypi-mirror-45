import unittest
import base64

from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.processing.impl.handshakestate import HandshakeState
from dissononce.processing.handshakepatterns.interactive.IK import IKHandshakePattern
from dissononce.processing.handshakepatterns.interactive.XX import XXHandshakePattern
from dissononce.processing.impl.symmetricstate import SymmetricState
from dissononce.processing.impl.cipherstate import CipherState
from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.hash.sha256 import SHA256Hash
from dissononce.dh.x25519.keypair import KeyPair
from dissononce.dh.x25519.public import PublicKey


class HandshakeStateTest(unittest.TestCase):
    def setUp(self):
        self.remote_static = PublicKey(
            base64.b64decode(
                b"8npJs5ulcmDmDaHZYflOveqXO73Gg2CzJySKvDs6qh4="
            )
        )
        self.local_static = KeyPair.from_bytes(
            base64.b64decode(
                b"MA9j0UP4lJwKWPtHcwSg+DTjM8HG0HI9k+vIMoxDiGHs59Xqht7dsss4K0PgyDKsxm6UwjwbG9Kgdit3iQiFRQ=="
            )
        )

        self.handshakestate = HandshakeState(
            SymmetricState(
                CipherState(
                    AESGCMCipher()
                ),
                SHA256Hash()
            ),
            X25519DH()
        )

    def test_protocol_name(self):
        self.handshakestate.initialize(
            handshake_pattern=IKHandshakePattern(),
            initiator=True,
            prologue=b"",
            s=self.local_static,
            rs=self.remote_static
        )
        self.assertEqual("Noise_IK_25519_AESGCM_SHA256", self.handshakestate.protocol_name)

    def test_stuff(self):
        self.handshakestate.initialize(
            handshake_pattern=XXHandshakePattern(),
            initiator=True,
            prologue=b"WA\x02\x01",
            s=self.local_static,
            rs=self.remote_static
        )
        # self.handshakestate.write_message()
