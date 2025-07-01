from __future__ import annotations

"""Helpers for loading trusted issuer public keys."""

from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey

# Directory containing PEM-encoded trust anchors, e.g. trust_anchors/OH.pem
ANCHORS_DIR = Path(__file__).resolve().parents[2] / "trust_anchors"


@lru_cache(maxsize=1)
def _load_anchors() -> Dict[str, EllipticCurvePublicKey]:
    """Load all trust anchors from :data:`ANCHORS_DIR`.

    Returns a mapping of issuer ID (file stem) to public key objects.
    Missing or unreadable directories yield an empty mapping.
    """
    anchors: Dict[str, EllipticCurvePublicKey] = {}
    if not ANCHORS_DIR.exists():
        return anchors
    for pem_file in ANCHORS_DIR.glob("*.pem"):
        try:
            key = load_pem_public_key(pem_file.read_bytes())
        except Exception:
            continue
        anchors[pem_file.stem.upper()] = key
    return anchors


def get_public_key(issuer_id: str) -> Optional[EllipticCurvePublicKey]:
    """Return the trust anchor for ``issuer_id`` if available."""
    if not issuer_id:
        return None
    anchors = _load_anchors()
    return anchors.get(issuer_id.upper())
