from ....dh.dh import DH
from .private import PrivateKey
from .public import PublicKey
from .keypair import KeyPair

from nacl.public import PrivateKey as NaclPrivateKey, Box, PublicKey as NaclPublicKey, SealedBox


class X25519DH(DH):
    def __init__(self):
        super(X25519DH, self).__init__("25519", 32)

    def dh(self, keypair, publickey):
        box = Box(NaclPrivateKey(keypair.private.data), NaclPublicKey(publickey.data))
        return box.shared_key()

    def create_public(self, data):
        return PublicKey(data)

    def generate_keypair(self, privatekey=None):
        if privatekey is None:
            private = NaclPrivateKey.generate()
        else:
            private = NaclPrivateKey(privatekey.data)

        public = private.public_key

        return KeyPair(
            PublicKey(
                public.encode()
            ),
            PrivateKey(
                private.encode()
            )
        )
