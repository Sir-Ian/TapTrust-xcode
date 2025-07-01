# tests/test_cbor.py

from verifier.decode.cbor import decode_payload


def test_decode_payload_plain_cbor():
    """decode_payload should handle plain CBOR maps."""
    payload = {"foo": "bar", "num": 123}
    import cbor2
    raw = cbor2.dumps(payload)

    result = decode_payload(raw)
    assert isinstance(result, dict)
    assert set(result.keys()) == set(payload.keys())
