from pathlib import Path

import cbor2
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

from verifier.crypto.verify import verify_signature
from verifier.config import SETTINGS_ENV, reload_settings

PRIVATE_KEY_PATH = Path(__file__).with_name("testkey_private.pem")


def sign_doc(doc: dict) -> bytes:
    key_bytes = PRIVATE_KEY_PATH.read_bytes()
    key = load_pem_private_key(key_bytes, password=None)
    return key.sign(cbor2.dumps(doc), ec.ECDSA(hashes.SHA256()))


def test_verify_valid_signature():
    doc = {
        "first_name": "Alice",
        "last_name": "Example",
        "dob": "1995-07-20",
        "issuing_state": "OH",
        "expiry": "2029-07-20",
    }
    sig = sign_doc(doc)
    payload = {"doc": doc, "signature": sig}
    assert verify_signature(payload) is True


def test_verify_corrupted_signature():
    doc = {"name": "Bob"}
    sig = sign_doc(doc)
    # Corrupt first byte
    bad_sig = b"\x00" + sig[1:]
    payload = {"doc": doc, "signature": bad_sig}
    assert verify_signature(payload) is False


def test_verify_unknown_issuer():
    doc = {"name": "Eve", "issuing_state": "ZZ"}
    sig = sign_doc(doc)
    payload = {"doc": doc, "signature": sig}
    assert verify_signature(payload) is False


def test_verify_disallowed_issuer(tmp_path, monkeypatch):
    doc = {
        "first_name": "Alice",
        "issuing_state": "OH",
    }
    sig = sign_doc(doc)
    payload = {"doc": doc, "signature": sig}

    cfg = tmp_path / "settings.yaml"
    cfg.write_text("allowed_issuers: [MD]")

    monkeypatch.setenv(SETTINGS_ENV, str(cfg))
    reload_settings()
    try:
        assert verify_signature(payload) is False
    finally:
        monkeypatch.delenv(SETTINGS_ENV, raising=False)
        reload_settings()
