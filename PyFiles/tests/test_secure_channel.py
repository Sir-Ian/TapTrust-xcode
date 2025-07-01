from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

import cbor2
from pycose.keys.ec2 import EC2Key

from verifier.crypto.secure import (
    generate_ephemeral_keypair,
    derive_session_keys,
    parse_device_engagement,
    aesgcm_from_key,
)


def test_key_derivation_matches_device_side():
    device_priv = ec.generate_private_key(ec.SECP256R1())
    device_cose = EC2Key._from_cryptography_key(device_priv.public_key())
    device_key_dict = cbor2.loads(device_cose.encode())
    de_payload = cbor2.dumps({"eDeviceKey": device_key_dict})

    device_pub = parse_device_engagement(de_payload)
    reader_priv, reader_pub = generate_ephemeral_keypair()
    reader_keys = derive_session_keys(reader_priv, device_pub)

    # Device performs the same derivation
    reader_pub_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), reader_pub
    )
    shared = device_priv.exchange(ec.ECDH(), reader_pub_key)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=64,
        salt=None,
        info=b"TapTrust Device Engagement",
    )
    expected = hkdf.derive(shared)
    assert reader_keys[0] == expected[:32]
    assert reader_keys[1] == expected[32:]

    # Round-trip test for AESGCM
    aes = aesgcm_from_key(reader_keys[0])
    nonce = b"\x00" * 12
    ct = aes.encrypt(nonce, b"hello", None)
    assert aes.decrypt(nonce, ct, None) == b"hello"
