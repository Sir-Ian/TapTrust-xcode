from __future__ import annotations

"""Helpers for ISO 18013-5 secure channel setup."""

import logging

import cbor2
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey,
    EllipticCurvePublicKey,
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from pycose.keys.ec2 import EC2Key

logger = logging.getLogger(__name__)


NDEF_AID = bytes.fromhex("D2760000850101")


def generate_ephemeral_keypair() -> tuple[EllipticCurvePrivateKey, bytes]:
    """Return a new P-256 private key and its public key bytes."""
    priv = ec.generate_private_key(ec.SECP256R1())
    pub = priv.public_key().public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )
    return priv, pub


def parse_device_engagement(payload: bytes) -> bytes:
    """Parse Device Engagement data and return the device public key bytes."""
    try:
        obj = cbor2.loads(payload)
    except Exception as e:  # pragma: no cover - parsing may fail with real data
        logger.debug("Device Engagement hex: %s", payload.hex())
        raise RuntimeError(f"Device Engagement decode failed: {e}") from None

    key_dict = obj.get("eDeviceKey") or obj.get(0)
    if not isinstance(key_dict, dict):
        raise RuntimeError("Device Engagement missing eDeviceKey")

    try:
        cose_key = EC2Key.from_dict(key_dict)
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"Invalid eDeviceKey: {e}") from None

    pub_bytes = b"\x04" + cose_key.x + cose_key.y
    # Validate by constructing a public key
    EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), pub_bytes)
    return pub_bytes


def derive_session_keys(
    reader_priv: EllipticCurvePrivateKey, device_pub: bytes
) -> tuple[bytes, bytes]:
    """Derive reader/device session keys via ECDH and HKDF."""
    dev_pub = EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), device_pub)
    shared = reader_priv.exchange(ec.ECDH(), dev_pub)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=64,
        salt=None,
        info=b"TapTrust Device Engagement",
    )
    key_material = hkdf.derive(shared)
    return key_material[:32], key_material[32:]


def aesgcm_from_key(key: bytes) -> AESGCM:
    """Return an :class:`AESGCM` instance for ``key``."""
    return AESGCM(key)
