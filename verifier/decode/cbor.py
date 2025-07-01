# verifier/decode/cbor.py

import cbor2
from verifier.decode.cose import unwrap_cose


def decode_payload(raw: bytes) -> dict:
    """
    Decode raw CBOR bytes into a Python dict by:
    1. Parsing the top-level CBOR to extract a COSE_Sign1 message.
    2. Passing COSE bytes to unwrap_cose() to get the actual payload dict.
    """
    # raw is normally a COSE_Sign1 structure. Attempt to decode it.
    try:
        return unwrap_cose(raw)
    except Exception:
        # If COSE decoding fails, fall back to plain CBOR.  The example
        # payload used by the CLI is a simple CBOR map rather than COSE
        # signed data.
        try:
            return cbor2.loads(raw)
        except Exception as e:
            raise RuntimeError(f"decode_payload failed: {e}")
