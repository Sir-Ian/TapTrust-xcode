# verifier/decode/cose.py


from pycose.messages import CoseMessage
import cbor2


def unwrap_cose(cose_bytes: bytes) -> dict:
    """
    Given raw COSE_Sign1 bytes, extract the payload as a Python dict.

    For now, we assume the payload inside COSE is itself CBOR-encoded.
    Later, we’ll feed the “payload” bytes into our JSON-like decode.

    Returns:
        A dict containing at least the “doc” and “signature” fields.
    """
    try:
        # Parse the COSE_Sign1 structure
        cose_msg = CoseMessage.decode(cose_bytes)
    except Exception as e:
        raise RuntimeError(f"Failed to decode COSE payload: {e}")

    # Extract the raw payload bytes (which we assume is CBOR again)
    raw_payload = cose_msg.payload
    if raw_payload is None:
        raise RuntimeError("COSE payload is empty")

    try:
        # Decode that CBOR payload into a Python dict
        data = cbor2.loads(raw_payload)
    except Exception as e:
        raise RuntimeError(f"Failed to decode inner CBOR payload: {e}")

    # Attach the signature bytes so verify_signature() can use them
    # pycose holds the signature in cose_msg.signature
    data["signature"] = cose_msg.signature

    return data

# COSE signature unwrap helpers
