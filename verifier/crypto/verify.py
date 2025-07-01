"""Signature verification helpers."""

import cbor2
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

from verifier.crypto.keys import get_public_key
from verifier.config import get_allowed_issuers


def verify_signature(parsed_payload: dict) -> bool:
    """Verify a parsed mDL payload.

    Parameters
    ----------
    parsed_payload: dict
        Result of :func:`decode_payload` which must contain ``doc`` and
        ``signature`` fields.

    Returns
    -------
    bool
        ``True`` if the signature matches the ``doc`` field, ``False``
        otherwise.
    """

    doc = parsed_payload.get("doc")
    signature = parsed_payload.get("signature")
    if doc is None or signature is None:
        return False

    try:
        data = cbor2.dumps(doc)
    except Exception:
        return False

    issuer = doc.get("issuing_state")

    allowed = get_allowed_issuers()
    if allowed and (issuer is None or issuer.upper() not in allowed):
        return False

    public_key = get_public_key(issuer)
    if public_key is None:
        return False

    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False


# ECDSA signature validation helpers
